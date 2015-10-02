var app = angular.module('pyngShop', ['ngAnimate', 'ngMaterial', 'ngRoute' ]);

var SETTINGS = {
	template : 'default',
	templatePath : function() {return ('/templates/' + this.template)},
	views : function() { return(this.templatePath() + '/views/')},
	partials : function() { return(this.templatePath() + '/partials/')}

};


app.config(function($routeProvider, $locationProvider){
	$locationProvider.html5Mode(true);

	console.log(SETTINGS.views());

	$routeProvider
		.when('/login', {
			controller: 'loginController',
			templateUrl: SETTINGS.views() + 'login.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/404', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.otherwise({
			redirectTo: '/404'
		});
});