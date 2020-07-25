Search.setIndex({docnames:["alg_spectrum","bluefog_ops","code_structure","devel_guide","docker","env_variable","index","install","performance","rationale","running","tensorflow_api","timeline","topo_api","torch_api"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":3,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,sphinx:56},filenames:["alg_spectrum.rst","bluefog_ops.rst","code_structure.rst","devel_guide.rst","docker.rst","env_variable.rst","index.rst","install.rst","performance.rst","rationale.rst","running.rst","tensorflow_api.rst","timeline.rst","topo_api.rst","torch_api.rst"],objects:{"bluefog.common":{topology_util:[13,0,0,"-"]},"bluefog.common.topology_util":{Dict:[13,1,1,""],FullyConnectedGraph:[13,2,1,""],GetWeights:[13,2,1,""],IsTopologyEquivalent:[13,2,1,""],List:[13,1,1,""],MeshGrid2DGraph:[13,2,1,""],PowerTwoRingGraph:[13,2,1,""],RingGraph:[13,2,1,""],StarGraph:[13,2,1,""],Tuple:[13,1,1,""]},"bluefog.torch":{DistributedAllreduceOptimizer:[14,2,1,""],DistributedBluefogOptimizer:[14,2,1,""],DistributedNeighborAllreduceOptimizer:[14,2,1,""],DistributedPullGetOptimizer:[14,2,1,""],DistributedPushSumOptimizer:[14,2,1,""],allgather:[14,2,1,""],allgather_nonblocking:[14,2,1,""],allreduce:[14,2,1,""],allreduce_nonblocking:[14,2,1,""],barrier:[14,2,1,""],broadcast:[14,2,1,""],broadcast_:[14,2,1,""],broadcast_nonblocking:[14,2,1,""],broadcast_nonblocking_:[14,2,1,""],broadcast_optimizer_state:[14,2,1,""],broadcast_parameters:[14,2,1,""],check_extension:[14,2,1,""],in_neighbor_ranks:[14,2,1,""],init:[14,2,1,""],load_topology:[14,2,1,""],local_rank:[14,2,1,""],local_size:[14,2,1,""],mpi_threads_supported:[14,2,1,""],nccl_built:[14,2,1,""],neighbor_allgather:[14,2,1,""],neighbor_allgather_nonblocking:[14,2,1,""],neighbor_allreduce:[14,2,1,""],neighbor_allreduce_nonblocking:[14,2,1,""],out_neighbor_ranks:[14,2,1,""],pair_gossip:[14,2,1,""],pair_gossip_nonblocking:[14,2,1,""],poll:[14,2,1,""],rank:[14,2,1,""],set_topology:[14,2,1,""],shutdown:[14,2,1,""],size:[14,2,1,""],synchronize:[14,2,1,""],timeline_context:[14,2,1,""],timeline_end_activity:[14,2,1,""],timeline_start_activity:[14,2,1,""],unified_mpi_window_model_supported:[14,2,1,""],win_accumulate:[14,2,1,""],win_accumulate_nonblocking:[14,2,1,""],win_create:[14,2,1,""],win_free:[14,2,1,""],win_get:[14,2,1,""],win_get_nonblocking:[14,2,1,""],win_lock:[14,2,1,""],win_mutex:[14,2,1,""],win_poll:[14,2,1,""],win_put:[14,2,1,""],win_put_nonblocking:[14,2,1,""],win_update:[14,2,1,""],win_update_then_collect:[14,2,1,""],win_wait:[14,2,1,""]},bluefog:{torch:[14,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","data","Python data"],"2":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:data","2":"py:function"},terms:{"37m":3,"boolean":14,"case":7,"class":[13,14],"default":[1,5,12,14],"export":5,"float":[13,14],"function":[1,3,5,6,12,14],"import":[0,3,6,13,14],"int":[13,14],"long":[3,5],"new":14,"return":[13,14],"static":14,"true":[6,14],Are:10,But:[0,3],For:[0,3,4,7,12,13,14],Not:14,One:[0,2,6,14],Ops:[5,6],That:6,The:[1,3,4,5,6,7,10,11,12,13,14],Then:[6,7],There:[5,11,12,13],These:[1,13],With:12,abc:13,abl:[3,10],about:[1,6,10],abov:[0,7,12],access:[6,7,14],accmul:14,accuml:5,accumul:[1,14],achiev:14,acquir:14,across:14,act:14,activ:[12,14],activity_nam:14,actual:[1,4,12],add:4,added:[8,9],address:[7,10],adjacenti:13,advantag:[0,6],after:[1,4,7,14],agent:[1,12],algorithm:[1,2,6,12,14],alia:13,alias:13,align:12,all:[0,1,3,4,5,6,7,10,12,13,14],allgath:14,allgather_nonblock:14,alloc:[1,10,12],allocate_output:12,allow:[0,1,14],allreduc:[0,6,12,14],allreduce_nonblock:14,almost:[0,1,10],alreadi:[4,14],also:[0,3,4,5,6,7],although:6,alwai:[1,13,14],among:0,anaconda3:3,ani:[0,1,3,5,10],anoth:[1,6,12,14],answer:[7,10],anyth:1,api:[1,2,6,13],appar:0,appli:14,applic:6,approach:0,apt:4,architectur:[0,6],arg:14,argument:[10,12,13,14],around:[13,14],arrow:[1,12],ascpect:0,ask:5,aspect:0,assign:1,associ:[0,1,14],assum:[7,13],assumpt:0,async:14,asynchron:[0,1,6],authent:10,auto:14,autograd:14,automat:[5,7],avail:7,averag:[0,1,6,12,14],avoid:[3,6,7],awar:7,back:12,backend:5,background:1,backpropag:[12,14],backward:12,barrier:[6,14],base:[0,3,6,12],basic:[1,12],batch:12,becaus:1,befor:[1,14],behavior:[1,14],belong:[0,14],below:12,better:[12,14],between:[0,1,6,12,13],bfrun:[4,6,12,14],bia:12,bidirect:13,block:[6,12,14],blog:1,bluefog:[0,2,13,14],bluefog_allgather_by_mpi:5,bluefog_allreduce_by_mpi:5,bluefog_broadcast_by_mpi:5,bluefog_cpu:4,bluefog_cpu_deploi:4,bluefog_cuda_hom:5,bluefog_cuda_includ:5,bluefog_cuda_lib:5,bluefog_gpu:4,bluefog_gpu_deploi:4,bluefog_log_hide_tim:5,bluefog_log_level:[3,5],bluefog_max_win_sent_length:5,bluefog_mpi_thread_level:5,bluefog_mpicxx_show:5,bluefog_nccl_hom:5,bluefog_nccl_includ:5,bluefog_nccl_lib:5,bluefog_neighbor_allgather_by_mpi:5,bluefog_neighbor_allreduce_by_mpi:5,bluefog_ops_on_cpu:5,bluefog_timelin:[5,14],bluefog_win_on_gpu:5,bluefog_with_nccl:[5,7],bluefoglib:[4,7],boll:14,bool:[13,14],both:12,bottleneck:[6,12],bridg:1,broadcast:[12,14],broadcast_:14,broadcast_nonblock:14,broadcast_nonblocking_:14,broadcast_optimizer_st:14,broadcast_paramet:14,browser:12,btye:0,buffer:[1,6,14],build:[1,5,6,7],build_ext:3,built:[1,4,5,7],builtin:13,bulk:6,bytep:6,cach:[6,7],calcul:1,call:[1,5,14],callabl:14,can:[0,1,3,4,5,6,7,10,12,13,14],cannot:[5,14],capabl:[4,5],carefulli:14,catogor:1,center_rank:13,central:[0,6,13],chang:[1,3,14],check:[1,4,6,7,10,13,14],check_extens:14,choic:14,chrome:12,cifar10:12,circl:1,circumst:1,clang:3,clean:4,clear:14,clearli:12,clone:[7,14],closest:13,coars:0,code:2,codebas:6,collect:[0,6,13,14],com:4,command:[3,4,7,10,12],comment:14,common:[6,13,14],commun:[0,5,6,7],communicaton:12,compar:6,comparison:6,compil:[3,14],complet:14,complex:0,compress:0,compuat:12,comput:[0,12,14],compute_averag:12,concaten:14,concurr:0,conda:[3,7],conduct:12,configur:7,connect:[1,6,10,12,13],connect_styl:13,consensu:[0,6],consid:[3,11],consider:0,consist:[0,3],construct:6,contain:[2,14],context:14,continu:10,contrast:3,contribut:6,control:[3,7],conveni:10,converg:6,coorespond:14,copi:[3,7],core:[0,6],correct:[3,4],correctli:[3,14],correspond:[1,5,13,14],cost:[0,6,7],could:4,cours:[0,2],cousin:1,cpu:[0,3,4,5],cpython:3,creat:[1,6,12,14],creation:14,cross:13,cuda:[4,5,7],curl:4,current:[0,7,14],custom:1,daemon:4,darwin:3,data:[0,1,7,14],dataset:[0,12],deactiv:12,deadlock:14,debug:3,decentr:[0,6,12],decid:14,decoupl:[1,6],dedic:[1,14],deep:6,defin:[3,5,6,13,14],definit:1,degrad:13,delai:0,depend:[4,7],deploy:4,deriv:[0,1],design:0,destin:14,detail:[3,4,5,7],detect:5,determin:[1,13,14],develop:[2,4,6,7,12],devic:4,dict:[13,14],dictionari:[13,14],didn:3,differ:[0,1,3,5,12,13,14],diffus:[0,6],digraph:[13,14],dimens:14,dir:[6,7],direct:[1,12],directli:[0,5,14],directori:3,distinguish:6,distribut:[4,6,12,14],distributedallreduceoptim:14,distributedbluefogoptim:[6,14],distributeddataparallel:6,distributedli:0,distributedneighborallreduceoptim:14,distributedpullgetoptim:14,distributedpushsumoptim:14,div_:6,divid:12,doc:[1,2],docker:[2,3,6],dockerfil:4,docstr:3,document:[2,4,5,10],doesn:[1,5],don:[0,1,5],done:14,down:14,download:[3,7],draw_circular:13,draw_spr:13,driver:4,dst_weight:[6,14],dual:0,due:[3,5],dure:[5,12,14],dynam:14,e2e:2,each:[0,1,6,10,12,13],earli:6,earlier:12,easi:6,easili:[3,6],echo:4,edg:1,edit:3,editor:3,effect:3,effici:[7,12],either:14,element:13,emploi:12,enabl:[5,12],encount:14,end:12,endact:14,enhanc:12,enqueu:12,enqueue_neighbor_allreduc:12,ensembl:0,enter:10,env:14,enviro:3,environ:[4,6,7],epoch:[3,5,14],equal:13,equival:[13,14],error:[0,4,5,7,10],establish:10,etc:[1,2,3,4,6],everi:10,exactli:1,exampl:[0,2,3,6,13,14],excel:0,except:[1,7,14],exchang:[1,12],exclus:[0,12,14],execut:[5,6,10,14],exist:[6,14],experi:12,explain:2,explan:[6,14],exploit:[0,12],explor:6,ext_nam:14,extent:7,extra:[7,14],facil:12,factor:13,fail:[7,10],fake:14,fals:[13,14],fast:6,faster:0,fatal:5,fault:[6,7,14],featur:[1,6,12],fetch:[1,14],few:[3,4],figur:[1,12],file:[3,4,6,12],file_nam:14,filenam:[5,12,14],filenan:3,fine:[0,3],fingerprint:10,finish:[11,12,14],first:[1,3,6,7,11,12,14],five:0,flag:[10,14],flexibl:0,focu:[1,4],focus:[0,1],folder:[2,3,5,6,7],follow:[1,3,4,5,6,7,12,14],forc:5,force_barri:14,forget:6,format:3,forward:12,found:[4,14],four:12,framework:6,free:14,friendli:6,from:[0,1,3,6,12,13,14],front:12,frontend:1,full:[7,12],fulli:[0,1,12,13],fullyconnectedgraph:13,funnction:14,funnel:5,further:12,furthermor:4,fusion:0,futur:0,gather:0,gcc:[3,7],gener:[3,12,13,14],get:[1,4,5,7,14],getweight:13,github:4,given:14,global:6,goal:6,going:6,good:5,googl:3,gpgkei:4,gpu:[0,3,4,5,10],gradient:[0,12,14],grain:0,graph:[1,13,14],greater:14,guarante:[6,11,14],guid:6,handl:14,happen:[12,14],has:[1,3,5,10,14],have:[0,3,4,5,7,13,14],heavili:[1,3],help:12,here:[0,1,4,14],heterogen:6,hide:5,hierarch:0,high:6,highli:[0,1,6,7],hold:14,home:[3,5],homogen:13,horovod:[2,6,12],host:[1,4,5,7,10],hostnam:10,how:[1,6,12],howev:[0,1,5,7],http:4,hub:7,idea:6,ident:14,identifi:14,illustr:[1,6,12],imag:[3,7],implement:[0,1,3,6,7,14],importantli:0,improv:12,in_neighbor_rank:[6,14],includ:[2,4,5,14],inclus:14,incom:1,inconsist:6,increas:12,increment:14,indegre:6,indentifi:12,independ:[7,12],index:13,indic:[1,12,14],infiniband:5,info:5,inform:[0,1,6,7,12,14],init:[6,14],initi:14,input:14,insid:[1,4],inst:13,instal:6,instanti:13,instead:[7,12,13,14],instruct:[3,7],integ:[13,14],interact:1,interest:[6,7],interfac:14,intern:[4,13],introduc:[1,6],introduct:1,invis:1,involv:14,is_weight:14,isol:4,isomorph:13,istopologyequival:13,iter:[0,6,14],its:[0,1,14],itself:14,join:6,json:12,just:[7,10],keep:[3,6],kei:[4,10,14],kind:[0,13],know:1,known:12,larg:0,last:[6,7],lastli:[3,7],latest:4,lauch:6,layer:12,lead:14,learn:[6,10],left:[12,13],len:6,length:13,less:0,let:5,level:[2,5,6],leverag:6,lib:3,librari:[3,4,5,7,14],like:[0,2,3,7,10,14],limit:3,line:[1,12],linear:13,link:7,linux:[3,7],list:[0,3,4,13,14],load:12,load_topolog:14,locaiton:5,local:[0,1,6,14],local_rank:14,local_s:14,locat:[5,7,12],log:5,look:2,loop:14,loosenli:1,loss:0,lot:[0,6],low:6,mac:3,machin:[3,6,10],maco:7,mai:[1,3,4,5,7,14],main:[1,2,5],mainli:12,make:[1,3,4,5,6,7,14],makefil:3,manag:14,mani:12,manual:[3,5],map:14,match:14,matrix:[12,13,14],matter:14,maxim:[6,7],maximum:5,mean:[0,3,14],memeori:14,memoeri:14,memori:[1,6,7,12,14],mention:[1,7],mere:3,meshgrid2dgraph:13,meshgrid:13,method:[0,1],middl:3,misc:5,mix:14,mnt:4,model:[0,6,14],modif:14,modifi:[3,6,14],more:[0,1,3,4,5,6,7,10,14],most:[0,1,3,5,6,7],move:7,mpi4pi:14,mpi:[1,3,5,6,7,10,14],mpi_lib:3,mpi_lock:5,mpi_neighbor_allreduc:12,mpi_put:5,mpi_thread_funnel:5,mpi_thread_multipl:5,mpi_thread_seri:5,mpi_thread_singl:5,mpi_threads_support:14,mpi_win:14,mpich:3,mpicxx:5,mpirun:[3,10],multi:[0,5,14],multipl:[0,3,5,6,12,14],must:[10,13,14],mutex:14,name:[1,3,4,6,13,14],named_paramet:14,nccl:[5,7,14],nccl_built:14,ncol:13,necessari:4,need:[1,4,5,6,7,12,14],negihbor:14,neighbor:[0,6,12,14],neighbor_allgath:14,neighbor_allgather_nonblock:14,neighbor_allreduc:[6,14],neighbor_allreduce_nonblock:14,neighbor_s:14,neighbor_weight:[13,14],neighbro_allreduc:14,neihbor:14,network:[1,4,5],networkx:[13,14],nice:1,node:[0,1,6,13,14],nois:0,non:[13,14],nonblock:[12,14],nonblockingli:14,none:[13,14],normal:[3,12],notabl:[1,12],note2:14,note:[1,14],noteabl:6,notic:[0,1,13,14],now:[3,14],nproc:7,nrow:13,number:[1,5,10,13,14],numer:1,object:14,observ:12,obtain:4,occur:12,often:3,one:[0,1,3,5,10,13,14],ones:[5,13],onli:[1,3,4,5,6,7,13,14],opeart:12,open:[3,7],openmpi:[3,6,7],oper:[5,6,12,14],ops:[1,5,14],optim:[6,14],option:[0,6],order:[3,4,7],organ:2,orient:3,origin:13,other:[0,5,6,7,10,12,13,14],otherwis:[3,14],our:[1,2,3,5,6,7],out:[1,3,14],out_neighbor:14,out_neighbor_rank:[6,14],outdegre:6,outgo:1,output:14,over:[0,1,10,14],overal:2,overflow:7,overlap:12,own:[1,6],packag:7,page:[6,7,10],pair:14,pair_gossip:14,pair_gossip_nonblock:14,pair_weight:14,paper:6,parallel:[0,6,12],param:[13,14],paramet:[0,6,14],parent:5,part:13,pass:3,passiv:14,password:10,passwordless:10,path:[5,12],peer:0,per:[10,14],perform:[6,12,14],permiss:10,phase:[3,12],pid:12,pip:[3,6],pipelin:0,pitfal:3,pkg_path:14,place:[3,14],plan:[0,3],platform:3,pleas:[1,3,4,6,7,11,14],point:13,poll:14,pop:4,popular:[0,6],posit:5,potenti:3,power:[6,12,13],power_two_r:14,powertworinggraph:[6,13],practic:12,prefer:3,prefix:7,preliminari:3,present:[7,14],prime:13,primit:12,print:6,privileg:4,probabl:6,problem:[0,6],process:[1,5,6,10,12,14],product:13,project:[0,2,3,4,6],prompt:10,properli:4,propog:12,provid:[0,3,4,6,13,14],prune:4,pull:[4,7,14],push:[6,14],put:[1,14],pylint:3,pylintrc:3,python3:3,python:[1,3,4,6,7,10,12,14],pytorch:[5,6,7,11],pytorch_average_consensu:4,pytorch_mnist:3,quantiz:0,question:10,quickli:6,rais:14,rang:6,rank:[1,6,12,13,14],rational:6,rdma:5,read:6,reader:4,readi:14,real:[3,6,12],realli:14,reason:[0,5,7],receiv:[1,7,12,14],recommend:[1,3,7],record:[12,14],red:1,reduc:[0,12,14],reduct:14,reinstal:3,relat:5,releas:4,relev:0,reli:[1,3,7],rememb:3,remot:[6,14],replic:0,repositori:[2,6,7],repres:[1,13],requir:[4,14],require_mutex:[6,14],reset:14,resili:0,respect:13,respons:[4,14],rest:[1,14],restart:4,result:[12,14],right:[3,13],ring:[0,6,13],ringgraph:[13,14],rma:14,root:[3,4,6,7,14],root_rank:14,rsa:10,run:[1,5,6,7,12,14],run_unittest:4,same:[0,1,7,10,13,14],save:3,scalabl:0,scalar:14,scale:[0,14],scratch:4,script:6,see:[1,3,5,6,10,12],segment:[7,14],select:[0,4],self:[1,14],self_weight:[13,14],send:[1,5,14],sender:1,serv:2,server1:10,server2:10,server3:10,server4:10,server:[0,6,10],servic:4,set:[5,7,10,12,13,14],set_topolog:[6,14],setup:[2,3,6],seven:14,sever:[3,5],sgd:[6,12,14],shape:[13,14],shard:0,share:[2,3,4,14],should:[3,7,13,14],show:[1,5,12],shut:14,shutdown:14,side:6,significantli:12,similar:[0,1,2,5,12],similarli:12,simpl:6,simultan:14,sinc:[1,10,14],site:3,six:[5,14],size:[5,6,13,14],sleep:14,slice:0,slightli:[0,1],small:1,smaller:13,some:[1,3,4,5,12,14],someth:3,sourc:[4,14],spars:0,spatial:0,speak:1,special:13,specif:5,specifi:[3,5,10,13,14],spectrum:6,squar:1,src_weight:14,ssh:4,stack:7,stage:[6,12],stale:0,standard:[1,5],star:13,stargraph:13,start:[3,12,14],startact:14,state:[12,14],state_dict:14,std:[3,7],step:[1,3,7,14],still:[0,5,6],store:[0,14],str:[13,14],string:13,strong:0,strongest:0,structur:[6,13,14],style:1,sub:12,subsect:7,succe:14,succeed:14,sudo:[4,7],suffici:7,sum:[1,6,14],summat:[1,14],support:[0,1,3,4,5,7,10,14],sure:[1,3,4,6,7,10,14],sychron:14,sync:[1,6,14],synchron:[0,1,6,12,14],system:[0,3,4,5,7,10],take:[3,14],taken:12,target_rank:14,task:12,techniqu:0,tee:4,tell:12,tempor:0,temporari:12,tensor:[0,1,5,6,12,14],tensor_nam:14,tensorflow:[0,7],tesnor:14,test:[2,4],than:[6,12,13],thank:0,them:1,theorat:6,therefor:4,thi:[0,1,2,3,4,5,6,7,10,12,13,14],thin:[10,14],thing:6,think:7,those:[1,6],though:7,thread:[5,12,14],three:[0,1],through:[0,1,5,6,14],throughout:3,tidi:3,time:[0,3,5,12,14],timelin:[5,6,14],timeline_context:14,timeline_end_act:14,timeline_fil:14,timeline_filenam:12,timeline_filename0:12,timeline_filename1:12,timeline_filename2:12,timeline_filename3:12,timeline_start_act:14,toler:6,too:5,top:2,topo1:13,topo2:13,topo:[13,14],topolog:[1,6,12,14],topology_fn:14,topology_util:[6,13,14],torch:[3,6],torch_ops_test:3,trace:[5,12],track:12,train:[0,6,10,14],travi:3,tune:5,tupl:13,turn:[3,5,14],tutori:1,two:[1,4,12,13,14],type:[1,4,6,10,13,14],typic:[0,10,14],ubuntu:4,unclear:5,under:[1,2,3,5,7],underli:14,understand:[6,12],undirect:12,unfornu:14,unifi:14,unified_mpi_window_model_support:14,uniform:1,uniformli:14,uniliter:13,uniqu:14,unittest:4,unless:[5,14],unlik:[0,3,5,6],unqiu:14,unrecover:14,until:[12,14],updat:[0,1,4,14],upon:1,usag:[1,2,5,6,7,10,14],usagem:2,use:[1,3,5,6,7,11,13,14],used:[4,7,12,13,14],useful:14,user:[0,2,3,4,7,13,14],uses:14,using:[3,4,7,10],util:[0,3,14],valu:[1,5,6,14],valueerror:14,variabl:[0,6,12,13,14],variou:3,vector:5,vender:3,verbos:[3,5],veri:[1,2],verifi:10,version:[3,7,13],version_id:4,via:12,virtual:[1,6,14],visibl:1,visual:12,wai:1,wait:[6,12,14],want:[5,6,10,14],warn:[3,5],weakest:0,weight:[1,13,14],weigt:12,welcom:6,well:[1,2,3,6,12],were:12,wheel:7,when:[4,12,13],whenev:3,where:[3,6,10,13,14],whether:14,which:[0,1,3,6,7,13,14],whole:[3,12],wieght:12,wiki:4,win:[1,5,14],win_accmul:14,win_accumul:[6,14],win_accumulate_nonblock:14,win_creat:[6,14],win_fre:14,win_get:14,win_get_nonblock:14,win_lock:14,win_mutex:14,win_op:[5,14],win_pol:14,win_put:[12,14],win_put_nonblock:14,win_upd:14,win_update_then_collect:[6,14],win_wait:14,window:[1,14],within:14,without:[3,10,14],won:7,word:12,would:10,wrap:[6,14],wrapper:[6,10,13,14],x_buff:6,yes:10,yet:[0,3,11],you:[1,3,4,5,6,7,10,12,14],your:[6,7,10,12,14],your_own_prefix:7,zero:[13,14],zero_init:[6,14]},titles:["The Spectrum of Distributed Machine Learning Algorithm","Bluefog Operations Explanation","The Structure of Codebase","BlueFog Development Guide","Bluefog Docker Usage","Bluefog Environment Variables","Bluefog","Installing Bluefog","Performance","Bluefog Rationale","Running Bluefog Through bfrun","Tensorflow Module (API Reference)","Bluefog Timeline","Topology Related Utility Functions","Torch Module (API Reference)"],titleterms:{"function":13,And:3,One:1,Ops:1,The:[0,2],Use:7,algorithm:0,allgath:1,allreduc:1,api:[11,14],bfrun:10,bluefog:[1,3,4,5,6,7,9,10,12],broadcast:1,build:[3,4],check:3,code:3,codebas:2,collect:1,collet:1,commun:[1,12],contain:4,continu:3,cpu:7,custom:3,debug:5,develop:3,directli:7,distribut:0,docker:[4,7],download:4,due:10,end:3,environ:[3,5],exampl:[4,12],explan:1,extens:3,failur:10,from:[4,7],github:7,gpu:7,guid:3,hub:4,iii:12,imag:4,instal:[3,4,5,7],integr:3,issu:10,learn:0,lint:3,local:3,logist:12,machin:0,modul:[11,14],neighbor:1,neighbor_allgath:1,neighbor_allreduc:[1,12],nvidia:4,one:12,oper:1,own:4,packag:3,perform:[5,8],pip:7,quick:6,rational:9,refer:[11,14],regress:12,relat:13,resnet:12,run:[3,4,10],runtim:4,side:[1,12],spectrum:0,ssh:10,start:6,structur:2,style:3,tensorflow:11,test:3,through:[7,10],timelin:12,topolog:13,torch:14,train:12,unit:3,usag:[4,12],util:13,variabl:5,win_accumul:[1,12],win_creat:1,win_fre:1,win_get:1,win_put:1,win_upd:1,win_update_then_collect:1,your:[3,4]}})