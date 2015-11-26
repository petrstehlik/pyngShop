var app = angular.module('pyngShop', ['ngRoute', 'angular.filter']);

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
	host : "localhost",
	port : "5000",
	version : "v1"
}