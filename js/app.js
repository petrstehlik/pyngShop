var app = angular.module('pyngShop', ['ngAnimate', 'ngMaterial', 'ngRoute' ]);

app.config(function($routeProvider){
	$routeProvider
		.when('/login', {
			controller: 'loginController',
			templateUrl: 'views/login.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/', {
			controller: 'homeController',
			templateUrl: 'templates/' + $themeName +'/views/home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/404', {
			controller: 'homeController',
			templateUrl: 'templates/' + $themeName +'views/home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.otherwise({
			redirectTo: '/404'
		});

});