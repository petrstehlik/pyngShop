app.directive("mainMenu", function() {
	return {
		scope: {
			section: '=',
		},
		templateUrl: SETTINGS.partials() + 'mainmenu.html'
	};
});

app.directive("userMenu", function() {
	return {
		scope: {
			section: '=',
		},
		controller : "userMenu",
		templateUrl: SETTINGS.partials() + 'usermenu.html'
	};
});


app.controller('mainMenuController', function($scope, $http, $q, api, auth){
	api.get("categories").then(function(r) {
		$scope.categories = r;
	})

	$scope.user = USER;

	$scope.addCategory = function(data, menu_item) {
		var d = $q.defer();
		console.log(data);
		var newCat = {}

		//data = data.toLowerCase().replace(/ /g, '_').replace(/[^\w-]+/g,'');

		if (menu_item == undefined) {
			newCat = {
				name : data,
				parent : null
			}
		} else {
			newCat = {
				name : data,
				parent : menu_item.category_id
			}
		}

		api.post('addcategory', newCat).then(function(r) {
			console.log(r);
			api.get("categories").then(function(r) {
				$scope.categories = r;
			})
		})
	}

	$scope.deleteCategory = function(cat) {
		console.log(cat);
		api.delete('categories', cat).then(function(res) {
			console.log(res);
			api.get("categories").then(function(r) {
				$scope.categories = r;
			})
		})
	}
	$scope.editCategory = function(data, menu_item) {
		var d = $q.defer();
		console.log(data);
		console.log(menu_item);
		menu_item["name"] = data;

		api.post('categories', menu_item).then(function(res) {
			console.log(res);
			api.get("categories").then(function(r) {
				$scope.categories = r;
			})
		})
	};
});

app.controller('userMenu', function($rootScope, $scope, $location, $route, cart, auth) {
	
	//$rootScope.$broadcast('restorecart');

	$scope.cart = cart.model;
	auth.get({admin : true})
	$scope.role = auth.user;
	USER.admin = auth.user.admin;

	$scope.logout = function() {
		auth.clear();
		$scope.role = auth.user;
		USER = {user: false, admin: false, editor: false};
		$location.path("/");
		$route.reload();
	}

	$scope.$on('addToCart', function(event, args) {
		//if($scope.cart.items.indexOf(args) == -1) {
			($scope.cart.items).push(args);
			$scope.cart.count++;
			console.log($scope.cart)
		//}

	})

	$rootScope.$on('applycart', function(event, args) {
		$scope.cart = cart.model;
	});
});

app.service('api', function($http, $log) {
	var url = "//" + API.host + ":" + API.port + "/" + API.version + "/";
	this.post = function(query, data) {
		var promise = $http({
			method : 'POST',
			headers: { 'Content-Type': 'application/json;charset=utf-8' },
			url : url + query,
			data : JSON.stringify(data)
		}).then(function successCallback(response) {
			return response["data"];
		}, function errorCallback(response) {
			$log.error(response);
			return response;
		});
		return promise;
	}

	this.delete = function(query, data) {
		var promise = $http({
			method : 'DELETE',
			headers: { 'Content-Type': 'application/json;charset=utf-8' },
			url : url + query,
			data : JSON.stringify(data)
		}).then(function successCallback(response) {
			return response["data"];
		}, function errorCallback(response) {
			$log.error(response);
			return response;
		});
		return promise;
	}

	this.get = function(query) {
		var promise = $http({
			method : 'GET',
			url : url + query,
		}).then(function successCallback(response) {
			return response["data"];
		}, function errorCallback(response) {
			$log.error(response);
			return response;
		});
		return promise;
	}
});

app.factory('cart', function ($rootScope, $localStorage) {
	var service = {
	    model : {
			count : 0,
			items : []
		},

        SaveState: function () {
           $localStorage.cart = angular.toJson(service.model);
           console.log(service)
           //console.log($localStorage.list)
        },

        RestoreState: function () {
            service.model = angular.fromJson($localStorage.cart);
        },

        InitCart: function() {
        	if (angular.fromJson($localStorage.cart) == undefined) {
        		// var tmp = {model : }
	        	$localStorage.cart = angular.toJson({count : 0, items : []});
        	}
        },
        CleanCart: function() {
	        	$localStorage.cart = angular.toJson({count : 0, items : []});
        }
    }

    $rootScope.$on("initcart", service.InitCart);
    $rootScope.$on("cleancart", service.CleanCart);
    $rootScope.$on("savecart", service.SaveState);
    $rootScope.$on("restorecart", service.RestoreState);

    return service;
});

app.service('auth', function($localStorage){
	var auth = {
		user : {
			admin : false,
			customer : false,
			cred : {
				details : {
					customer_id : null
				}
			}
		},
		store : function(cred, date) {
			auth.user = {"cred" : cred}

			if (cred.admin) {
				auth.user.admin = true;
				auth.user.expiry = date;
				$localStorage.user = angular.toJson(auth.user)
			} else {
				auth.user.customer = true;
				$localStorage.user = angular.toJson(auth.user)
			}
		},
		get : function() {
			auth.user = angular.fromJson($localStorage.user)
			//console.log(auth.user)
			if (auth.user == undefined) {
				console.log("cleaning")
				auth.clear();
				auth.get();
			}

			return auth.user;
		},
		verify : function(cred, role) {
			return angular.fromJson($localStorage.user)
		},
		clear : function() {
			$localStorage.user = angular.toJson({user : {admin : false,customer : false, cred : {
				details : {
					customer_id : null
				}
			}}})
			auth.get();
		}
	}

	return auth;
});

app.service('newProd', function(){

	var product = {};

	var storeProduct = function (cat) {
		product = cat;
		console.log(product);
	}

	var getProduct = function() {
		return product;
	}

	var removeProduct = function() {
		product = {};
	}

	return {
		storeProduct : storeProduct,
		getProduct : getProduct,
		removeProduct : removeProduct
	};
});

app.factory('page', function(){
  var title = "Default";
  return {
    title: function() { return title; },
    setTitle: function(newTitle) { title = newTitle; }
  };
});


app.filter("total", function() {
	return function(items) {
	  	var total = 0, i = 0;
	  	for (i = 0; i < items.length; i++) {
	  		total += items[i]['price'] * items[i]['quantity'];
	  	}

	  	return total;
	}
});