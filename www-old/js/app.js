app.config(function($routeProvider, $locationProvider){

	$locationProvider.html5Mode(false);

	$routeProvider
		.when('/', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			resolve: {
			}
		})
		.when('/404', {
			controller: 'notFoundController',
			templateUrl: SETTINGS.views() + '404.html',
			resolve: {
//				isLoggedIn: checkLogin
			}
		})
		.when('/login', {
			controller: 'loginController',
			templateUrl: SETTINGS.views() + 'login.html',
			resolve: {
			}
		})
		.when('/cart', {
			controller: 'cartController',
			templateUrl: SETTINGS.views() + 'cart.html',
			resolve: {
				//exists : checkPage
			}
		})
		.when('/checkout', {
			controller: 'checkoutController',
			templateUrl: SETTINGS.views() + 'checkout.html',
			resolve: {
				//exists : checkPage
			}
		})
		.when('/checkout/success', {
			controller: 'successController',
			templateUrl: SETTINGS.views() + 'success.html',
			resolve: {
				//exists : checkPage
			}
		})
		.when('/invoice', {
			controller: 'invoiceController',
			templateUrl: SETTINGS.views() + 'invoice.html',
			resolve: {
				//exists : checkPage
			}
		})
		.when('/admin', {
			controller: 'ordersController',
			templateUrl: SETTINGS.views() + 'admin.html',
			resolve: {
				//exists : function() {return check.admin()}
			}
		})
		.when('/admin/orders', {
			controller: 'ordersController',
			templateUrl: SETTINGS.views() + 'orders.html',
			resolve: {
				//exists : function() {return check.admin()}
			}
		})
		.when('/admin/orders/:order_id', {
			controller: 'orderDetailController',
			templateUrl: SETTINGS.views() + 'orderDetail.html',
			resolve: {
				//exists : function() {return check.admin()}
			}
		})
		.when('/account', {
			controller: 'accountController',
			templateUrl: SETTINGS.views() + 'account.html',
			resolve: {
				//exists : function() {return check.admin()}
			}
		})
		.when('/p/addproduct', {
			controller: 'newProductController',
			templateUrl : SETTINGS.views() + 'newproduct.html'
		})
		.when('/:category*/p/:product', {
			controller: 'productController',
			templateUrl: SETTINGS.views() + 'product.html',
			resolve: {
			//	exists : function() {return check.category()}
			}
		})
		.when('/:category*', {
			controller: 'categoryController',
			templateUrl: SETTINGS.views() + 'category.html',
			resolve: {
				//exists : function() {return check.category()}
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
		.otherwise({
			redirectTo: '/404'
		});
});

app.service('check', function($location, $routeParams, api, auth) {
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
		},
		admin : function() {
			if (auth.user.admin) {
				api.post("checklogin", auth).then(function (response) {
					console.log(response)
				})
			}
		}
	}
	// if ($routeParams.page != "login" || $routeParams.page != "404") {
	// 	$location.path("/404");
	// }
})

app.run(function($rootScope, $location, auth, api, editableOptions) {
	editableOptions.theme = 'default';
	USER.admin = auth.user.admin;
	USER.customer = auth.user.customer;
    $rootScope.$on( "$routeChangeStart", function(event, next, current) {
    	auth.get();
		if (next.controller == "adminController" || next.controller == "ordersController" || next.controller == "orderDetailController") {
			if(!auth.user.admin) {
				$location.path("/");
			}

			api.post("checklogin", auth.user.cred.session).then(function (response) {
				console.log(response)
				if (response != "1")
					$location.path("/")
			})

		}
      if (!USER.admin) {
        // no logged user, redirect to /login
        if ( next.templateUrl === "partials/login.html") {
        } else {
          //$location.path("/login");
        }
      }
    });
  });

app.directive('showtab',
    function () {
        return {
            link: function (scope, element, attrs) {
                element.click(function(e) {
                    e.preventDefault();
                    $(element).tab('show');
                });
            }
        };
    });

app.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                    console.log(attrs);
                });
            });
        }
    };
}]);

app.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl){
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
        })
        .error(function(){
        });
    }
}]);

app.filter('capitalize', function() {
    return function(input) {
    	input = input.replace('_', ' ').replace('-', ' ');
      	return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
    }
});


