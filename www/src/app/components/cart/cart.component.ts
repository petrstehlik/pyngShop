import { Component, OnInit  } from '@angular/core';

import { CartService } from 'app/services/cart.service';
import { ShippingService } from 'app/services/shipping.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss'],
  providers : [CartService, ShippingService]
})
export class CartComponent implements OnInit {

	cart = [];
	shipping = [];
	total = 0;
	selectedShipping = 0;
	addressValid = false;

	constructor(private cartService :  CartService,
			   private shippingService : ShippingService) { }

	ngOnInit() {

		this.cart = this.cartService.get();
		this.getTotal();
		this.getShipping();
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
		for (let item of this.cart) {
			this.total += item["product"]["price"] * item["quantity"];
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

}
