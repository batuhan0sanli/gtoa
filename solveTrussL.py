# ---------------------------------------
# solveTrussL v1.0 by Dr. Hakan ÖZBAŞARAN
# ---------------------------------------

# Gerekli kütüphaneler import ediliyor
# ------------------------------------
from openseespy.opensees import *
# ------------------------------------


# some Python interpreters return the axial force as a list
# "flt" is to fix that eleResponse(i,"axialForce") problem
# ---------------------------------------------------------
def flt(x):
    if type(x) is list:
        return(x[0])
    else:
        return(x)
# ---------------------------------------------------------


# OpenSees kütüphanesini kullanarak 2 ve 3 boyutlu kafes sistemleri çözer.
# -------------------------------------------------------------------------------
# Girdi biçimi aşağıdaki yığılmış liste şeklindedir.
# [
#     [malzemenin elastisite modülü, birim ağırlığı],
#     [[düğüm numarası, x koordinatı, y, varsa z], ...],
#     [[mesnetin düğüm numarası, x yönü tutulu mu? (1 veya 0), y, varsa z], ...],
#     [1 numaralı kesitin alanı, 2 numaralı kesitin alanı, ...],
#     [[çubuk numarası, kesit numarası, başlangıç düğümü, bitiş düğümü], ...]
#     [
#         1 numaralı yükleme durumu
#         [[düğüm numarası, x yönündeki kuvvet, y, varsa z], ...],
#         2 numaralı yükleme durumu
#         [[düğüm numarası, x yönündeki kuvvet, y, varsa z], ...],
#         ...
#     ]    
# ]
# -------------------------------------------------------------------------------
# [w, [[r1,u1,n1,s1], [r2,u2,n2,s2], ...]] biçiminde çıktı verir.
#     w  : yapı ağırlığı
#     r1 : 1 numaralı yükleme için mesnet reaksiyonları
#     u1 : 1 numaralı yükleme için düğüm yer değiştirmeleri
#     n1 : 1 numaralı yükleme için çubuk kuvvetleri
#     s1 : 1 numaralı yükleme için çubuk gerilmeleri
#     r2 : 2 numaralı yükleme için mesnet reaksiyonları
#     u2 : ...
# -------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
def solveTrussL(struct):
    # ---------- STRUCTURE DATA ----------
    elasMod=struct[0][0] # Young's modulus
    unitW=struct[0][1] # unit weight
    nodes=struct[1] # nodes
    supports=struct[2] # supports
    sections=struct[3] # sections
    members=struct[4] # members
    cases=struct[5] # loading cases
    # ------------------------------------
    
    nd=len(nodes[0])-1 # problem dimension
    
    # ----------------------- MODEL -----------------------
    wipe() # remove existing model
    model("basic","-ndm",nd,"-ndf",nd) # set modelbuilder
    
    if nd==2: # planar truss
        for i in nodes: # define nodes
            node(i[0],i[1],i[2])
        for i in supports: # define supports
            fix(i[0],i[1],i[2])
    if nd==3: # spatial truss
        for i in nodes: # define nodes
            node(i[0],i[1],i[2],i[3])
        for i in supports: # define supports
            fix(i[0],i[1],i[2],i[3])
    
    uniaxialMaterial("Elastic",1,elasMod) # define material
    for i in members: # define members
        element("Truss",i[0],i[2],i[3],sections[i[1]-1],1)
    # -----------------------------------------------------
    
    # --------- DEFINE ANALYSIS PARAMETERS ----------
    system("BandSPD") # create SOE
    numberer("RCM") # create DOF number
    constraints("Plain") # create constraint handler
    integrator("LoadControl",1.0) # create integrator
    algorithm("Linear") # create algorithm
    analysis("Static") # create analysis object
    # -----------------------------------------------
    
    timeSeries("Constant",1) # create "Constant" TimeSeries
    results=[] # container for the results
    
    # ------------------------------ LOADING CASE LOOP ------------------------------
    for case in cases:
        
        # ------------- LOADING AND ANALYSIS -------------
        pattern("Plain",1,1) # create a plain load pattern
        if nd==2: # planar truss
            for i in case: # loads
                load(i[0],i[1],i[2])
        if nd==3: # spatial truss
            for i in case: # loads
                load(i[0],i[1],i[2],i[3])

        sol=analyze(1) # perform the analysis
        if sol<0: return(["error"]) # if analysis fails return "error"
        # ------------------------------------------------
        
        # ---------------------------- PREPARE THE OUTPUT ---------------------------
        r=[] # support reactions
        reactions("-dynamic")
        for i in range(1,len(supports)+1):
            r.append(nodeReaction(i))
        u=[] # node displacements
        for i in range(1,len(nodes)+1):
            u.append(nodeDisp(i))
        n=[] # axial forces
        s=[] # member stresses
        for i in range(1,len(members)+1):
            force=flt(eleResponse(i,"axialForce")) # member force
            n.append(force)
            a=[sections[j[1]-1] for j in members if j[0]==i][0] # member section area
            s.append(force/a) # member stress
        # ---------------------------------------------------------------------------
        
        # --- RESHAPE THE LISTS ---
        r=[i for j in r for i in j]
        u=[i for j in u for i in j]
        # -------------------------
        
        results.append([r,u,n,s]) # save the results for this loading case
        remove("loadPattern",1) # delete the previously defined loading case
        reset() # reset the model to its unloaded initial state
    # -------------------------------------------------------------------------------
    
    # ------------------ CALCULATE THE STRUCTURE WEIGHT ------------------
    v=0 # volume of the structure
    for i in members:
        n1=[j for j in nodes if i[2]==j[0]][0][1:]
        n2=[j for j in nodes if i[3]==j[0]][0][1:]
        v+=sections[i[1]-1]*sum([(c2-c1)**2 for c1,c2 in zip(n1,n2)])**0.5
    w=unitW*v
    # --------------------------------------------------------------------
    
    return([w,results]) # return the results
# -----------------------------------------------------------------------------------