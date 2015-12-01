app.controller('ordersController', function($scope, auth, api) {
	$scope.hello = "hello";

	api.get("orders").then(function(r) {
		$scope.orders = r;		
	})

	api.get("warehouse").then(function(r) {
		$scope.products = r;
	})

	$scope.toggleMan = 0;

	$scope.submitMan = function(man) {
		console.log(man);
		api.post("warehouse", man).then(function(r) {
			console.log(r)
			api.get("warehouse").then(function(r) {
				$scope.products = r;
				$scope.toggleMan = 0;
			})
		});
	}

	$scope.removeMan = function(man) {
		console.log(man)
		api.delete('warehouse', {manufacturer_id : man}).then(function(r) {
			api.get("warehouse").then(function(r) {
				$scope.products = r;
			})
		})
	}

	api.get("admins").then(function(r) {
		$scope.admins = r;
	})
	$scope.submitAdmin = function(admin) {
		console.log(admin);
		api.post("admins", admin).then(function(r){
			api.get("admins").then(function(r) {
				$scope.admins = r;
			})
		})
	}

	$scope.deleteAdmin = function(admin) {
		api.delete('admins', admin).then(function(r) {
			api.get("admins").then(function(r) {
				$scope.admins = r;
			})
		})
	}
})

app.controller('orderDetailController', function($scope, $routeParams, auth, api){
	console.log($routeParams)
	api.get("orders/" + $routeParams.order_id).then(function (r) {
		$scope.invoice = r;
	})
});