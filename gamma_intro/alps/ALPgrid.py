import matplotlib.pyplot as plt
import matplotlib as mpl
from gammapy.modeling import Fit
import numpy as np
import astropy.units as u
import multiprocessing


class ALPgrid:
    def __init__(self, dataset_per_gridpoint=None):
        
        self.dataset_per_gridpoint     = check_keys_in_dict(dataset_per_gridpoint)
        
    
    
    def get_TS_per_gridpoint(self):
        logL_dict = {}
        TS_dict   = {}
        min_logL  = None
        
        i = 0
        for mg in self.dataset_per_gridpoint.keys():
            idataset        = self.dataset_per_gridpoint[mg]
            
            if i > 0:
                idataset.models.parameters.value = results.parameters.value
        
            fit             = Fit(optimize_opts={'strategy': 0})
            results         = fit.run(idataset)
            logL            = idataset.stat_sum()
            logL_dict[mg]   = logL
            TS_dict[mg]     = logL
            if min_logL is None:
                min_logL      = logL
            elif logL < min_logL:
                min_logL = logL
        # subtract the minimum to get the TS
        for i in TS_dict.keys(): TS_dict[i] -= min_logL
        self.min_logL            = min_logL
        self.logL_per_gridpoint  = logL_dict
        self.TS_per_gridpoint    = TS_dict

        
        
    def get_CL_per_gridpoint(self, simulated_TS=None):
    
        try:
            self.TS_per_gridpoint
        except:
            raise ValueError("No TS values for each grid point! Please run 'get_TS_per_gridpoint()'")   
    
        CL_per_gridpoint = {}
        # if None simulated TS  in imput, 
        # we will assumed WIlks theorem to be true
        if simulated_TS is None:
            TS_cdf = partial(chi2.cdf, df=2)
        else:
            print("To be completed")
            
        for mg in self.TS_per_gridpoint.keys():
            TS_obs               = self.TS_per_gridpoint[mg]
            CL_per_gridpoint[mg] = TS_cdf(TS_obs) #CDF_from_list(sim_TSs, TSobs)
        self.CL_per_gridpoint = CL_per_gridpoint
            
        
    def get_sigma_per_gridpoint(self):
        try:
            self.CL_per_gridpoint
        except:
            raise ValueError("No CL values for each grid point! Please run 'get_CL_per_gridpoint()'")   
            
        sigma_per_gridpoint = {}
        # first we deal with Sigma = Infinity
        maxCL = 0
        for CL in self.CL_per_gridpoint.values():
            sigm  = scipys.erfinv(CL)*np.sqrt(2)
            if sigm  != np.inf and CL> maxCL:
                maxCL = CL
        # now we compute the number of sigmas
        for mg in self.CL_per_gridpoint.keys():   
            CL   = self.CL_per_gridpoint[mg]
            sigm = scipys.erfinv(CL)*np.sqrt(2)
            if sigm == np.inf:
                sigm = scipys.erfinv(maxCL)*np.sqrt(2)
            sigma_per_gridpoint[mg] = sigm
        self.sigma_per_gridpoint = sigma_per_gridpoint
    
 


    def plot_grid(self, fig=None,ax=None, show=None, contour=False,scatter=True,
                         values=True, lines=False, point=None, **kwargs):
        ''' plot likelihood reuslt for m and g

        '''
        m_vals = u.Quantity( [i[0] for i in list( self.dataset_per_gridpoint.keys() )] ) 
        g_vals = u.Quantity( [i[1] for i in list( self.dataset_per_gridpoint.keys() )] )
        if fig is None or ax is None:
            fig,ax = FigSetup(Shape='Rectangular',
                    xunit = "eV",
                    yunit = "1 / GeV",
                    mathpazo=True,
                    g_min=np.min(g_vals.value), g_max=np.max(g_vals.value),
                    m_min=np.min(m_vals.value ), m_max=np.max(m_vals.value))
        
        # X and Y values
        x      = np.unique( u.Quantity( [i[0] for i in self.dataset_per_gridpoint.keys()] ) )
        y      = np.unique( u.Quantity( [i[1] for i in self.dataset_per_gridpoint.keys()] ) ) 
        X, Y   = np.meshgrid( x.value, y.value)        
        # Z values and Z label
        if show == "TS":
            try:
                Z      = self.TS_per_gridpoint.values()
                zlabel = '$-2 \Delta \;  \log \; (\;  L \;)$'
            except:
                raise ValueError("No TS values for each grid point! Please run 'get_TS_per_gridpoint()''")
        if show == "logL":
            try:
                Z      = self.logL_per_gridpoint.values()
                zlabel = '$-2 \;  \log \; (\;  L \;)$'
            except:
                raise ValueError("No TS values for each grid point! Please run 'get_TS_per_gridpoint()''")
        if show == "CL":
            try:
                Z      = self.CL_per_gridpoint.values()
                zlabel = 'CL'
            except:
                raise ValueError("No CL values for each grid point! Please run 'get_CL_per_gridpoint()''")
        if show == "sigma":
            try:
                Z      = self.sigma_per_gridpoint.values()
                zlabel = r'Significance / $\sigma$'
            except:
                raise ValueError("No sigma values for each grid point! Please run 'get_sigma_per_gridpoint()''")              
        
        if show is None:
            scatter = True
        else:
            Z      = np.array( list( Z ) )
            Z      = Z.transpose()
            Z      = np.reshape(Z, X.shape )
            # contour lines
            if lines:
                co    = ax.contour(  X, Y, Z, **kwargs)
                ax.clabel(co, inline=1, fontsize=20,fmt='%1.2f',colors='black')
            # contour map
            if contour:
                co_f  = ax.contourf( X,Y , Z, 500, cmap="rainbow",vmax=np.max(Z))
                cbar  = fig.colorbar(co_f)
                cbar.set_label(zlabel, rotation=90,size=30)
            # show Z value for each point 
            if values:
                for i, txt in enumerate(Z):
                    for j, itxt in enumerate(txt):
                        itxt = round(itxt,2)
                        ax.annotate(itxt, (X[i][j], Y[i][j]),color="black",fontsize=20)
            # show a given point on the plot
            if point is not None:
                ax.scatter(true_val[0],true_val[1],c="black",s=50,label="True value")
                ax.legend(loc='best')
            
            
        if scatter:
            ax.scatter(X,Y, s=50, facecolors='white', edgecolors='black',linewidths=2)

        return fig, ax

    
    
def check_keys_in_dict(input_dict):
    
    sorted_dict = {}
    
    x      = u.Quantity( [i[0] for i in input_dict.keys() ] )
    x_unit = x.unit
    y      = u.Quantity( [i[1] for i in input_dict.keys() ] )
    y_unit = y.unit
    
    
    # CHECK DIMENSIONS AND 
    # ASSIGN MASS AND COUPLING LIST
    m_list, g_list = None, None
    # FOR X LIST
    try:
        test   = x_unit/u.eV
        test   = test.to( u.dimensionless_unscaled)
        m_list = x
    except:
        try:
            test   = x_unit*u.GeV
            test   = test.to( u.dimensionless_unscaled)
            g_list = x
        except:
            raise ValueError("Parameter dimension should be eV for the ALP mass and 1/GeV for the coupling!")
    # FOR Y LIST
    try:
        test   = y_unit/u.eV
        test   = test.to( u.dimensionless_unscaled)
        m_list = y
    except:
        try:
            test   = y_unit*u.GeV
            test   = test.to( u.dimensionless_unscaled)
            g_list = y
        except:
            raise ValueError("Parameter dimension should be eV for the ALP mass and 1/GeV for the coupling!")
    ##
    if m_list is None or g_list is None:
            raise ValueError("Parameter dimension should be eV for the ALP mass and 1/GeV for the coupling!") 
            
    m_list   = np.sort( np.unique( m_list ) )
    g_list   = np.sort( np.unique( g_list ) )
    grid     = np.meshgrid(m_list,g_list)
    for im,ig in zip(  np.ravel( grid[0] )  , np.ravel( grid[1] ) ):
        im_converted   = im.to(u.eV)
        ig_converted   = ig.to( 1/u.GeV)
        try:
            sorted_dict[im_converted,ig_converted] = input_dict[im,ig]
        except:
            sorted_dict[im_converted,ig_converted] = input_dict[ig,im]
        
    return sorted_dict

    
    

def previous_limits(ax,plot_HESS=True,plot_Fermi=True,
                        plot_Mrk421=True, plot_Helioscopes=True,
                        plot_Chandra = True):
    if plot_HESS:
        HESS(ax)
    if plot_Mrk421:
        Mrk421(ax)
    if plot_Fermi:
        Fermi(ax)
    if plot_Chandra:
        Chandra(ax)
    if plot_Helioscopes:
        Helioscopes(ax)
    return ax

def HESS(ax,text_label=r'{\bf HESS}',text_pos=[3e-8,3e-11],col=[0.0, 0.55, 0.3],text_col="w",fs=16,zorder=0.2,text_on=True):
    # HESS arXiv:[1304.0700]
    dat = np.loadtxt("AxionPhoton/HESS.txt")
    FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on)
    return


def Mrk421(ax,text_label=r'{\bf Mrk 421}',text_pos=[3e-9,6e-11],col=[0.4, 0.6, 0.1],text_col='w',fs=12,zorder=0.26,text_on=True):
    # Mrk 421 arXiv:[2008.09464]
    dat = np.loadtxt("AxionPhoton/Mrk421.txt")
    FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on)
    return ax

def Chandra(ax,text_label=r'{\bf Chandra}',text_pos=[1.01e-11,1.5e-12],col= [0.0, 0.3, 0.24],text_col=[0.0, 0.3, 0.24],fs=15,zorder=0.1,text_on=True):
    # Chandra arXiv:[1907.05475]
    dat = np.loadtxt("AxionPhoton/Chandra.txt")
    FilledLimit(ax,dat,text_label,text_pos=text_pos,col=col,text_col=text_col,fs=fs,zorder=zorder,text_on=text_on)
    return

def Fermi(ax,text_label=r'{\bf Fermi}',text_pos=[4.02e-9,1.2e-11],col=[0.0, 0.42, 0.24],text_col='w',fs=15,zorder=0.24,text_on=True):
    # Fermi NGC1275 arXiv:[1603.06978]
    Fermi1 = np.loadtxt("AxionPhoton/Fermi1.txt")
    Fermi2 = np.loadtxt("AxionPhoton/Fermi2.txt")
    plt.fill_between(Fermi1[:,0],Fermi1[:,1],y2=1e0,edgecolor=col,facecolor=col,zorder=zorder,lw=3)
    plt.fill(Fermi2[:,0],1.01*Fermi2[:,1],edgecolor=col,facecolor=col,lw=3,zorder=zorder)
    Fermi1 = np.loadtxt("AxionPhoton/Fermi_bound.txt")
    Fermi2 = np.loadtxt("AxionPhoton/Fermi_hole.txt")
    plt.plot(Fermi1[:,0],Fermi1[:,1],'k-',alpha=0.5,lw=2,zorder=zorder)
    plt.plot(Fermi2[:,0],Fermi2[:,1],'k-',alpha=0.5,lw=2,zorder=zorder)
    if text_on:
        plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,ha='left',va='top',clip_on=True)
    return

def Helioscopes(ax,col=[0.5, 0.0, 0.13],fs=25,projection=False,RescaleByMass=False,text_on=True):
    # CAST arXiv:[1705.02290]
    y2 = ax.get_ylim()[1]
    if RescaleByMass:
        rs1 = 1.0
        rs2 = 0.0
    else:
        rs1 = 0.0
        rs2 = 1.0
    dat = np.loadtxt("AxionPhoton/CAST_highm.txt")
    plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=2,zorder=1.49,alpha=1)
    plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor='k',facecolor=col,zorder=1.49,lw=0.1)
    mf = dat[-2,0]
    gf = dat[-2,1]
    dat = np.loadtxt("AxionPhoton/CAST.txt")
    plt.plot(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),'k-',lw=2,zorder=1.5,alpha=1)
    plt.fill_between(dat[:,0],dat[:,1]/(rs1*2e-10*dat[:,0]+rs2),y2=y2,edgecolor='none',facecolor=col,zorder=1.5,lw=0.0)
    gi = 10.0**np.interp(np.log10(mf),np.log10(dat[:,0]),np.log10(dat[:,1]))/(rs1*2e-10*mf+rs2)
    plt.plot([mf,mf],[gf,gi],'k-',lw=2,zorder=1.5)
    if text_on==True:
        if rs1==0:
            plt.text(4e-8,8.6e-11,r'{\bf CAST}',fontsize=fs+2,color='w',rotation=0,ha='center',va='top',clip_on=True)
        else:
            plt.text(4e-8,8e-11,r'{\bf CAST}',fontsize=fs+4,color='w',rotation=0,ha='center',va='top',clip_on=True)

    if projection:
        # IAXO arXiv[1212.4633]
        IAXO_col = 'purple'
        IAXO = np.loadtxt("AxionPhoton/Projections/IAXO.txt")
        plt.plot(IAXO[:,0],IAXO[:,1]/(rs1*2e-10*IAXO[:,0]+rs2),'--',linewidth=2.5,color=IAXO_col,zorder=0.5)
        plt.fill_between(IAXO[:,0],IAXO[:,1]/(rs1*2e-10*IAXO[:,0]+rs2),y2=y2,edgecolor=None,facecolor=IAXO_col,zorder=0,alpha=0.3)
        if text_on==True:
            if rs1==0:
                plt.text(0.35e-1,0.2e-11,r'{\bf IAXO}',fontsize=fs,color=IAXO_col,rotation=45,clip_on=True)
            else:
                plt.text(0.7e-2,0.12e1,r'{\bf IAXO}',fontsize=fs,color=IAXO_col,rotation=-18,clip_on=True)
    return

def FigSetup(xlab=r'$m_a$',ylab='$|g_{a\gamma}|$',\
                 xunit = 'neV', yunit = '$GeV$^{-1}$',
                 g_min = 1.0e-19,g_max = 1.0e-6,\
                 m_min = 1.0e-12,m_max = 1.0e7,\
                 lw=2.5,lfs=45,tfs=25,tickdir='out',\
                 Grid=False,Shape='Rectangular',\
                 mathpazo=False,TopAndRightTicks=False,\
                xtick_rotation=20.0,tick_pad=8,\
             FrequencyAxis=False,N_Hz=1,upper_xlabel=r"$\nu_a$ [Hz]",**freq_kwargs):

    xlab +=' [ '+xunit+' ] '
    ylab +=' [ '+yunit+' ] '
    #plt.rcParams['axes.linewidth'] = lw
    #plt.rc('text', usetex=True)
    #plt.rc('font', family='serif',size=tfs)

    if mathpazo:
        mpl.rcParams['text.latex.preamble'] = [r'\usepackage{mathpazo}']

    if Shape=='Wide':
        fig = plt.figure(figsize=(16.5,5))
    elif Shape=='Rectangular':
        fig = plt.figure(figsize=(16.5,11))

    ax = fig.add_subplot(111)

    ax.set_xlabel(xlab,fontsize=lfs)
    ax.set_ylabel(ylab,fontsize=lfs)

    ax.tick_params(which='major',direction=tickdir,width=2.5,length=13,right=TopAndRightTicks,top=TopAndRightTicks,pad=tick_pad)
    ax.tick_params(which='minor',direction=tickdir,width=1,length=10,right=TopAndRightTicks,top=TopAndRightTicks)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim([m_min,m_max])
    ax.set_ylim([g_min,g_max])

    locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=50)
    locmin = mpl.ticker.LogLocator(base=10.0, subs=np.arange(2, 10)*.1,numticks=100)
    ax.xaxis.set_major_locator(locmaj)
    ax.xaxis.set_minor_locator(locmin)
    ax.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())

    locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100)
    locmin = mpl.ticker.LogLocator(base=10.0, subs=np.arange(2, 10)*.1,numticks=100)
    ax.yaxis.set_major_locator(locmaj)
    ax.yaxis.set_minor_locator(locmin)
    ax.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())

    plt.xticks(rotation=xtick_rotation)

    if Grid:
        ax.grid(zorder=0)

    if FrequencyAxis:
        UpperFrequencyAxis(ax,N_Hz=N_Hz,tickdir='out',\
                           xtick_rotation=xtick_rotation,\
                           xlabel=upper_xlabel,\
                           lfs=lfs/1.3,tfs=tfs,tick_pad=tick_pad-2,**freq_kwargs)

    return fig,ax

def FilledLimit(ax,dat,text_label='',col='ForestGreen',edgecolor='k',zorder=1,\
                    lw=2,y2=1e0,edgealpha=0.6,text_on=False,text_pos=[0,0],\
                    ha='left',va='top',clip_on=True,fs=15,text_col='k',rotation=0,facealpha=1):
    plt.plot(dat[:,0],dat[:,1],'-',color=edgecolor,alpha=edgealpha,zorder=zorder,lw=lw)
    plt.fill_between(dat[:,0],dat[:,1],y2=y2,edgecolor=None,facecolor=col,alpha=facealpha,zorder=zorder)
    if text_on:
        plt.text(text_pos[0],text_pos[1],text_label,fontsize=fs,color=text_col,ha=ha,va=va,clip_on=clip_on,rotation=rotation,rotation_mode='anchor')
    return

