app.config(function($routeProvider, $locationProvider){

	$locationProvider.html5Mode(false);

	$routeProvider
		.when('/login', {
			controller: 'loginController',
			templateUrl: SETTINGS.views() + 'login.html',
			resolve: {
				isLoggedIn: checkLogin
			}
		})
		.when('/', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			resolve: {
				isLoggedIn: checkLogin
			}
		})
		.when('/cart', {
			controller: 'cartController',
			templateUrl: SETTINGS.views() + 'cart.html',
			resolve: {
				isLoggedIn: checkLogin
				//exists : checkPage
			}
		})
		.when('/checkout', {
			controller: 'checkoutController',
			templateUrl: SETTINGS.views() + 'checkout.html',
			resolve: {
				isLoggedIn: checkLogin
				//exists : checkPage
			}
		})
		.when('/checkout/success', {
			controller: 'successController',
			templateUrl: SETTINGS.views() + 'success.html',
			resolve: {
				isLoggedIn: checkLogin
				//exists : checkPage
			}
		})
		.when('/invoice', {
			controller: 'invoiceController',
			templateUrl: SETTINGS.views() + 'invoice.html',
			resolve: {
				isLoggedIn: checkLogin
				//exists : checkPage
			}
		})
		.when('/:category*/p/:product', {
			controller: 'productController',
			templateUrl: SETTINGS.views() + 'product.html',
			resolve: {
				isLoggedIn: checkLogin,
				exists : function(check) {return check.category()}
			}
		})
		.when('/:category*', {
			controller: 'categoryController',
			templateUrl: SETTINGS.views() + 'category.html',
			resolve: {
				isLoggedIn: checkLogin,
				exists : function(check) {return check.category()}
			}
		})
		
		// .when('/:page/:subpage', {
		// 	controller: 'pageController',
		// 	templateUrl: SETTINGS.views() + 'page.html',
		// 	resolve: {
		// 		isLoggedIn: checkLogin,
		// 		exists : function(check) {return check.category()}
		// 	}
		// })
		.when('/404', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			resolve: {
				isLoggedIn: checkLogin
			}
		})
		.otherwise({
			redirectTo: '/404'
		});
});

checkLogin = function() {
	if (USER.admin) {
		console.log('You\'re loggen in as admin');
	}
	else {
		console.log("You are nobody");
	}
}

app.factory('check', function($location, $routeParams, api) {
	return {
		category : function(path) {
			console.log($location.path())
			api.post("checkpage", path).then(function(response) {
				console.log(response);
			});
		},
		product : function(path) {
			api.post("checkpage", path).then(function(response) {
				console.log(response);
			})
		}
	}
	// if ($routeParams.page != "login" || $routeParams.page != "404") {
	// 	$location.path("/404");
	// }
})

app.run(function($rootScope, $location) {
    $rootScope.$on( "$routeChangeStart", function(event, next, current) {
      if (!USER.admin) {
        // no logged user, redirect to /login
        if ( next.templateUrl === "partials/login.html") {
        } else {
          $location.path("/login");
        }
      }
    });
  });
