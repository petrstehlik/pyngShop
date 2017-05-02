import { Component, OnInit  } from '@angular/core';
import { Router  } from '@angular/router';

import { CartService } from 'app/services/cart.service';
import { ShippingService } from 'app/services/shipping.service';
import { UserService } from 'app/services/user.service';
import { OrderService } from 'app/services';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss'],
  providers : [CartService, ShippingService, UserService, OrderService]
})
export class CartComponent implements OnInit {

	cart = [];
	shipping = [];
	total = 0;
	selectedShipping = -1;
	addressValid = false;
	customer = null;

	constructor(private cartService :  CartService,
			   private shippingService : ShippingService,
			   private userService : UserService,
			   private orderService : OrderService,
			   private router : Router) { }

	ngOnInit() {

		this.cart = this.cartService.get();
		this.getTotal();
		this.getShipping();
		this.customer = this.userService.current();
	}

	removeItem(item : Object) {
		this.cartService.removeItem(item["product"]);
		this.cart = this.cartService.get();
		this.getTotal();
	}

	updateItem(item : Object) {
		this.cartService.updateItem(item["product"], item["quantity"]);
		this.cart = this.cartService.get();
	}

	onChange(item : Object) {
		this.getTotal();
		this.updateItem(item);
	}

	getTotal() {
		this.total = 0;
		this.cart = this.cartService.get();
		for (let item of this.cart) {
			this.total += item["product"]["price"] * item["quantity"];
		}

		for (let item of this.shipping) {
			if (item["id"] == this.selectedShipping) {
				this.total += item["price"];
			}
		}

	}

	getShipping() {
		this.shippingService.fetchAll().subscribe(
			data => {
				this.shipping = data;
			},
			err => {
				console.log(err);
			}
		)
	}

	userValid() {
		let c = this.customer["customer"];
		if (c["first_name"] &&
			c["last_name"] &&
			c["email"] &&
			c["address1"] &&
			c["phone"] &&
			c["state"] &&
			c["postal_code"])
			return true;

		else
			return false;
	}

	placeOrder() {
		console.log({
			"shipping" : this.selectedShipping,
			"ordered_products" : this.cart
		});

		this.orderService.add({
			"shipping" : {"id" : this.selectedShipping},
			"ordered_products" : this.cart
		}).subscribe(
			data => {
				console.log(data);
				this.cartService.clear();
				this.router.navigate(['/']);
			},
			err => {
				console.log(err);
			}
		)
	}

}
