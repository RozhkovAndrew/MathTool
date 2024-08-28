import eel
import os
dirnameF = os.path.dirname(__file__)  #путь исполняемого файла
eel.init(os.path.join(dirnameF, "web/")) #путь к каталогу со страницами
@eel.expose  #чтобы от js принимать функции
def transform_fraction(a):
    #Сократить дробь (в итоге будет несокращаемая неправильная (если >1) дробь)
    def sokr_drob(i,d,n):
        nod=1
        if d!=0:
            for j in range(2,d+1):
                if d%j==0 and n%j==0:
                    nod=j
            d,n=d//nod+i*n//nod,n//nod
        else:
            d,n=i,1
        return d,n
    #Разделение числа на целую и дробную часть
    if a.find(".")!=-1:
        i,d=a.split(".")
        n=10**len(d)
    elif a.find(",")!=-1:
        i,d=a.split(",")
        n=10**len(d)  
    else:
        i,d,n=a,'0',1
    #Проверка на периодическую дробь (проверять дробную часть на скобки) и подсчет числителя и знаменателя
    if "(" not in d:
        d,n=sokr_drob(int(i),int(d),n)
    else:
        do,dp=d.replace(")","").split("(")
        n,m=10**len(do),10**len(dp)-1
        if do=="":
            d,n=sokr_drob(int(i),int(dp),m)
        else:
            d,n=sokr_drob(int(i),int(do)*m+int(dp),n*m)
    #Вывод числителя и знаменателя через /
    eel.get_fraction('{0:.0f}'.format(d),'{0:.0f}'.format(n))

@eel.expose
def transform_root(t,p):
    a,m=int(t),int(p)
    A=[[],[]]
    fullPart,rootPart,i=1,1,2
    #Формируем двумерный массив из множителей
    while (a**2)!=1 and a!=0:
        if a%i==0:
            if i not in A[0]:
                A[0].append(i)
                A[1].append(1)
            else: A[1][-1]+=1
            a=a//i
        else: i+=1
    #извлекаем целую часть из корня и то что остается под корнем
    if m==0:
        fullPart="нет"
        rootPart=""
    elif m>0:
        for i in range(0,len(A[0])):
            fullPart*=A[0][i]**(A[1][i]//m)
            rootPart*=A[0][i]**(A[1][i]%m)
    else:
        for i in range(0,len(A[0])):
            fullPart*=1/(A[0][i]**(A[1][i]//(-1*m)))
            rootPart*=1/(A[0][i]**(A[1][i]%(-1*m)))
    if rootPart==1: rootPart="" #Ничего не записываем под корнем если он равен 1
    #Формируем ответ в зависимости от степени и знака числа под корнем
    if a==0 and m!=0: eel.get_root('0','')
    elif a<0 and m%2==0: eel.get_root(str(fullPart*complex(0,1)),str(rootPart))
    elif a<0 and m%2==1: eel.get_root(str(fullPart*(-1)),str(rootPart))
    else: eel.get_root(str(fullPart),str(rootPart))

@eel.expose
def transform_Xroots(a,b,c):
    if a=="":a="0"
    if b=="":b="0"
    if c=="":c="0"
    a,b,c,Res=int(a),int(b),int(c),""
    #Проверка на нули в коэффициентах (быстрые решения)
    if a==0 and b==0 and c==0: Res=("бесконечное количество решений")
    elif a==0 and b==0: Res=("решений нет")
    elif b==0 and c==0: Res="x=0"
    elif a==0: Res=("x=-c/b=-{1}/{0}={2:2f}".format(b,c,(-1*c/b)))
    else:
        if b%2==0:
            Disc=b*b/4-a*c
            Res="D/4=b*b/4-a*c={1}*{1}/4-{0}*{2}={3}".format(a,b,c,Disc)+"\n"
            if Disc<0:
                Res+="D/4 < 0. корней нет в действительных числах\n"
                Res+="X1=(-b/2-√(D/4))/a = (-{1}-j√{2})/{0} = {3:.2f}".format(a,b/2,(-1*Disc),(-1*b/2-Disc**0.5)/a)+"\n"
                Res+="X2=(-b/2+√(D/4))/a = (-{1}+j√{2})/{0} = {3:.2f}".format(a,b/2,(-1*Disc),(-1*b/2+Disc**0.5)/a)+"\n"
            elif Disc==0:
                Res+="D/4 = 0. 1 корень\n"
                Res+="X=(-b)/2a = (-{1})/{0} = {2:.2f}".format(a,b,(-1*b/2)/a)+"\n"
            else:
                Res+="D/4 > 0. 2 корня\n"
                Res+="X1=(-b/2-√(D/4))/a = (-{1}-√{2})/{0} = {3:.2f}".format(a,b/2,Disc,(-1*b/2-Disc**0.5)/a)+"\n"
                Res+="X2=(-b/2+√(D/4))/a = (-{1}+√{2})/{0} = {3:.2f}".format(a,b/2,Disc,(-1*b/2+Disc**0.5)/a)+"\n"
        if b%2==1:
            Disc=b*b-4*a*c
            Res="D=b*b-4*a*c={1}*{1}-4*{0}*{2}={3}".format(a,b,c,Disc)+"\n"
            if Disc<0:
                Res+="D < 0. корней нет в действительных числах\n"
                Res+="X1=(-b-√D)/2a = (-{1}-j√{2})/(2*{0}) = {3:.2f}".format(a,b,(-1*Disc),(-1*b-Disc**0.5)/(2*a))+"\n"
                Res+="X2=(-b+√D)/2a = (-{1}+j√{2})/(2*{0}) = {3:.2f}".format(a,b,(-1*Disc),(-1*b+Disc**0.5)/(2*a))+"\n"
            elif Disc==0:
                Res+="D = 0. 1 корень\n"
                Res+="X=(-b)/2a = (-{1})/(2*{0}) = {2:.2f}".format(a,b,(-1*b/2)/a)+"\n"
            else:
                Res+="D > 0. 2 корня\n"
                Res+="X1=(-b-√D)/2a = (-{1}-√{2})/(2*{0}) = {3:.2f}".format(a,b,Disc,(-1*b-Disc**0.5)/(2*a))+"\n"
                Res+="X2=(-b+√D)/2a = (-{1}+√{2})/(2*{0}) = {3:.2f}".format(a,b,Disc,(-1*b+Disc**0.5)/(2*a))+"\n"
    #Вывод решения и результата            
    eel.get_Xroots(Res)
            
@eel.expose
def transform_Reduct(num,den):
    n=max(abs(num.find(".")-len(num))-1,abs(den.find(".")-len(den))-1)
    num,den,nod=int(float(num)*10**n),int(float(den)*10**n),1
    for j in range(2,min(num,den)+1):
        if num%j==0 and den%j==0:
            nod=j
    num,den=num//nod,den//nod
    eel.get_Reduct(str(num),str(den))
    
eel.start("main.html", size=(850, 950)) #отображение выбранной страницы (из каталога)