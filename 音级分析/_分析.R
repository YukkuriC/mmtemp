library(ggplot2)

type=c('equal','pyth','pure')
name=c('十二平均律','五度相生律','纯律')

# 自然音级
{
  fdata=read.csv('自然音级_freq.csv')
  
  # 频率分布图
  plot_seq=ggplot()+theme_bw()+
    theme(panel.grid.minor = element_blank(),axis.text.x = element_text(hjust=1,angle=45))+
    labs(y='自然音级(A4=440Hz)',x='十二平均律音级/距A4音分数')+scale_color_hue('律制')+
    scale_y_continuous(breaks=c(-100,100))+
    scale_x_log10(
      breaks=fdata$equal,
      labels=c("C4 / -900","D4 / -700","E4 / -500","F4 / -400","G4 / -200","A4 / 0","B4 / 200",
               "C5 / 300","D5 / 500","E5 / 700","F5 / 800","G5 / 1000","A5 / 1200","B5 / 1400",
               "C6 / 1500")
      )+
    geom_segment(data=fdata,aes(y=-1,yend=1,x=pyth,xend=pyth,color="五度相生律"))+
    geom_segment(data=fdata,aes(y=-1,yend=1,x=pure,xend=pure,color="纯律"))
  
  pdf('自然音级_频率.pdf',10,4,family="GB1")
  print(plot_seq)
  graphics.off()
  
  # 音程间频率差
  plot_diff=ggplot()+theme_bw()+
    theme(panel.grid.minor = element_blank(),axis.text.x = element_text(hjust=1,angle=45))+
    labs(y='音级间相差音分数',x='十二平均律音级/距A4音分数')+scale_color_hue('律制')+
    scale_y_continuous(breaks=seq(-20,20,2))+
    scale_x_log10(
      breaks=fdata$equal,
      labels=c("C4 / -900","D4 / -700","E4 / -500","F4 / -400","G4 / -200","A4 / 0","B4 / 200",
               "C5 / 300","D5 / 500","E5 / 700","F5 / 800","G5 / 1000","A5 / 1200","B5 / 1400",
               "C6 / 1500")
    )+geom_hline(aes(yintercept=0))+
    geom_line(data=fdata,aes(x=equal,y=log(pyth/equal,2)*1200,color='五度相生律'))+
    geom_line(data=fdata,aes(x=equal,y=log(pure/equal,2)*1200,color='纯律'))
  
  pdf('自然音级_频率差.pdf',10,5,family="GB1")
  print(plot_diff)
  graphics.off()
  
  # 二度音程分布图
  plot_dist=ggplot()+theme_bw()+theme(panel.grid.minor = element_blank())+
    labs(x='音程长度/音分',y='密度')+scale_color_hue('律制')+
    scale_x_continuous(breaks=c(100,200),limits=c(50,250))
  for(i in 1:3){
    plot_dist=plot_dist+eval(parse(
      text=sprintf(
        'stat_density(aes(x=log(fdata$%s[2:nrow(fdata)]/fdata$%s[1:(nrow(fdata)-1)],2)*1200,color="%s"),bw=6,geom="line")',
        type[i],type[i],name[i]
      )
    ))
  }
  
  pdf('自然音级_音程分布.pdf',7,6,family="GB1")
  print(plot_dist)
  graphics.off()
}

# 变化音级
{
  fdata=read.csv('变化音级_freq.csv')
  fdata$offset=(1:nrow(fdata))%%2
  
  # 频率分布图
  plot_seq=ggplot()+theme_bw()+
    theme(panel.grid.minor = element_blank(),axis.text.x = element_text(hjust=1,angle=45))+
    labs(y='变化音级(A4=440Hz)',x='音级(十二平均律)')+scale_color_hue('律制')+
    scale_y_continuous(breaks=c(0,1),labels=c('#','b'))+
    scale_x_log10(
      breaks=c(
        246.941650628062, 261.625565300599, 277.182630976872, 293.664767917408,
        311.126983722081, 329.62755691287, 349.228231433004, 369.994422711634,
        391.995435981749, 415.304697579945, 440, 466.16376151809, 493.883301256124,
        523.251130601197, 554.365261953744
      ),
      labels=c(
        '#B3 bC4', 'C4', '#C4 bD4', 'D4', '#D4 bE4', 'E4 bF4', '#E4 F4', 
        '#F4 bG4', 'G4', '#G4 bA4', 'A4', '#A4 bB4', 'B4 bC5', '#B4 C5', '#C5'
      )
    )+
    geom_segment(data=fdata,aes(y=offset-0.5,yend=offset+0.5,x=pure,xend=pure,color="纯律"))+
    geom_segment(data=fdata,aes(y=offset-0.5,yend=offset+0.5,x=pyth,xend=pyth,color="五度相生律"))
  
  pdf('变化音级_频率.pdf',10,4,family="GB1")
  print(plot_seq)
  graphics.off()
  
  # 音程间频率差
  plot_diff=ggplot()+theme_bw()+
    theme(panel.grid.minor = element_blank(),axis.text.x = element_text(hjust=1,angle=45))+
    labs(y='音级间相差音分数',x='十二平均律音级/距A4音分数')+
    scale_color_hue('律制')+scale_linetype('升降号')+
    scale_y_continuous(breaks=seq(-50,50,5))+
    scale_x_log10(
      breaks=c(
        246.941650628062,  277.182630976872,
        311.126983722081, 329.62755691287, 349.228231433004, 369.994422711634,
        415.304697579945, 466.16376151809, 493.883301256124,
        523.251130601197, 554.365261953744
      ),
      labels=c(
        '#B3 bC4',  '#C4 bD4', '#D4 bE4', 'bF4', '#E4', 
        '#F4 bG4', '#G4 bA4', '#A4 bB4', 'bC5', '#B4', '#C5'
      )
    )+geom_hline(aes(yintercept=0))+
    geom_line(data=fdata[fdata$offset==1,],aes(x=equal,y=log(pyth/equal,2)*1200,color='五度相生律',linetype='b'))+
    geom_line(data=fdata[fdata$offset==1,],aes(x=equal,y=log(pure/equal,2)*1200,color='纯律',linetype='b'))+
    geom_line(data=fdata[fdata$offset==0,],aes(x=equal,y=log(pyth/equal,2)*1200,color='五度相生律',linetype='#'))+
    geom_line(data=fdata[fdata$offset==0,],aes(x=equal,y=log(pure/equal,2)*1200,color='纯律',linetype='#'))
  
  pdf('变化音级_频率差.pdf',10,5,family="GB1")
  print(plot_diff)
  graphics.off()
}
