var _setInterval=setInterval;
setInterval=function(a,b){
	if(a.toString().indexOf("debugger")!=-1){
		return 
	}
	_setInterval(a,b);
}