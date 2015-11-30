var app = angular.module('pyngShop', ['ngRoute', 'angular.filter', 'ngStorage']);

var SETTINGS = {
	template : 'default',
	templatePath : function() {return ('templates/' + this.template)},
	views : function() { return(this.templatePath() + '/views/')},
	partials : function() { return(this.templatePath() + '/partials/')}
};

var USER = {
	user : false,
	editor : false,
	admin : true
}

var API = {
	host : "pcstehlik.fit.vutbr.cz",
	port : "5000",
	version : "v1"
}