var app = angular.module('pyngShop', ['ngAnimate', 'ngMaterial', 'ngRoute' ]);

var SETTINGS = {
	template : 'default',
	templatePath : function() {return ('/templates/' + this.template)},
	views : function() { return(this.templatePath() + '/views/')},
	partials : function() { return(this.templatePath() + '/partials/')}

};