

class Param:
       s_1=0
       s_c=0
       s_w=0
       n=0
       Zr=0
       ET_max=0
       nZr=0
       eta=0
       g_plus=0;  
       a=0;         
       b0=0;         
       s_xi=0;
## piecewise linear function for normalized loss rate (ET) under well-watered conditions
def nerl(s, p):
	if s<p.s_c:
		 y=(p.eta)*(float(s)/float(p.s_c));
	if s>=p.s_c:
   		 y= p.eta;
        return y

class outputsim:
    s=[];
    vol_irr=[];
    dt_irr=[];
    nirr=0;
    R_norm=[];
    I_norm=[];
    ET_norm=[];
    stress=[];
    LQ_norm=[];
    b=[];
    g=[];
    
## Blaney-Criddle equation
def et_Blaney_Criddle(T,p,rhmin,n_N,Ud):
    Ndays=len(T)
    et=[0] * Ndays
    for t in range(Ndays):
        a=0.0043*rhmin[t]-n_N[t]-1.41
        b=0.82-0.0041*rhmin[t]+1.07*n_N[t]+0.066*Ud[t]-0.006*rhmin[t]*n_N[t]-0.0006*rhmin[t]*Ud[t]
        f=p[t]*(  0.46*T[t]+8.13);
        et[t]=a+(b*f);
    return et

## Penman-Monteith equation 
def et_PM(T,delta,rn,u2,es,ea,gamma):
    Ndays=len(T)
    et=[0] * Ndays
    cn=900
    cd=0.34
    for t in range(Ndays):
        num=0.4*delta[t]*(rn[t]-0.1*rn[t])+gamma*(cn/(T[t]+273))*u2[t]*(es[t]-ea[t])
        den=delta[t]+gamma*(1+cd*u2[t])
        et[t]=num/den
    return et
    
## Water Productivity
def WP(y,v,r,ds):
    return float(y)/float(v+r+ds)

## Yeld - empirical equation (Vico2011)
def Y_vico2011(ETseas,Ymax,ETseas_50,a):
    num=Ymax* (ETseas**a)
    den=(ETseas_50**a + ETseas**a);
    return float(num)/float(den)

## Yeld - dichotomic pocess (Vico2013)
def crop_development_simulation_R_ET_Z_I(p,Ndays,s_start,R,ET_max,Zr,I):
    outs=soil_moisture_simulation_R_ET_Z_I(p,Ndays,s_start,R,ET_max,Zr,I)
    s=outs.s
    ns=len(s)
    b = [0] * ns
    g = [0] * ns
    b[0]=p.b0
    out=outputsim
    for t in range(ns):
        if t>0:
            if s[t]>=p.s_xi:
                g[t]=p.g_plus
            if s[t]< p.s_xi:
                g[t]=p.g_plus* ((float(s[t])/float(p.s_xi))**p.a);
            b[t]=b[t-1]+g[t]
    out.b=b;
    out.g=g;
    return out         
 ## soil water balance equation               
def soil_moisture_simulation_R_ET_Z_I(p,Ndays,s_start,R,ET_max,Zr,I):
    out=outputsim()
    s = [0] * (Ndays+1)
    s[0]=s_start
    vol_irr=[0] * (Ndays+1)
    t_irr=[]
    dt_irr=[]
    ET_norm=[0] * (Ndays+1)
    LQ_norm=[0] * (Ndays+1)
    R_norm=[0] * (Ndays+1)
    I_norm=[0] * (Ndays+1)
    dsdt=[0] * (Ndays+1)
    stress=[0] * (Ndays+1)
    stress[0]=0
    for t in range(Ndays):
        p.Zr=Zr[t]
        p.ET_max=ET_max[t]
        p.nZr = p.n * p.Zr
        p.eta= float(p.ET_max)/float(p.n *p.Zr)
        R_norm[t]=float(R[t])/float(p.nZr); 
        I_norm[t]=float(I[t])/float(p.nZr);
        ET_norm[t] = nerl(s[t],p);
        if I_norm[t]>0 :
            if len(t_irr)>1 :
                dt_irr.append(t-t_irr[len(t_irr)-1])
            t_irr.append(t)
        if t>0:
            vol_irr[t]=vol_irr[t-1]+I_norm[t]*p.nZr
        if t==0:
            vol_irr[t]=I_norm[t]*p.nZr
        dsdt[t] = R_norm[t]+I_norm[t] - ET_norm[t]
        if s[t]+dsdt[t]>p.s_1:## Check for leakage
            LQ_norm[t] = ((s[t]+dsdt[t])-p.s_1);
            dsdt[t] = dsdt[t] - LQ_norm[t];
##        Increment soil moisture
        s[t+1] = s[t] + dsdt[t];
##%%      stress
        q=2;
        if s[t+1]<=p.s_w :
            stress[t+1]=1;
        if s[t+1]>p.s_w and s[t+1]<= p.s_c:
            tmp=float(p.s_c-s[t+1])/float(p.s_c-p.s_w)         
            stress[t+1]=tmp**q;
        if s[t+1]> p.s_c :
            stress[t+1]=0;
    nirr=len(t_irr)
    out.s=s
    out.vol_irr=vol_irr
    out.dt_irr=dt_irr
    out.nirr=nirr
    out.R_norm=R_norm
    out.I_norm=I_norm
    out.ET_norm=ET_norm
    out.stress=stress
    out.LQ_norm=LQ_norm

    return out
            
         
