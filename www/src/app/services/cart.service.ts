import { Injectable } from '@angular/core';

/**
  * Operations with cart
  *
  * \note Only within local storage.
  */
@Injectable()
export class CartService {

    cart : Array<Object> = [];

    constructor() {
        this.refresh();
    }

    clear() {
        localStorage.removeItem("cart");
        this.cart = [];
    }

    save() {
        localStorage.setItem("cart", JSON.stringify(this.cart));
    }

    refresh() {
        this.cart = JSON.parse(localStorage.getItem("cart"));

        if (this.cart == null) {
            this.cart = [];
        }
    }

    length() {
    	let len = 0;
    	for (let item of this.cart)
    		len += item["quantity"];
        return len;
    }

    get() {
		return JSON.parse(localStorage.getItem("cart"));
    }

    addItem(item : Object, quantity : Number) {
        for (let product of this.cart) {
        if (quantity > product["quantity"]) {
            return;
        }
            if (product["product"]["id"] == item["id"]) {
                product["quantity"] += quantity;
                this.save();
                return;
            }
        }

        this.cart.push({"product" : item, "quantity" : quantity});

        this.save();
    }

    updateItem(item : Object, quantity : Number) {
		for (let product of this.cart) {
            if (product["product"]["id"] == item["id"]) {
                product["quantity"] = quantity;
                this.save();
                return;
            }
        }

        this.save();

    }

    removeItem(item : Object) {
    	let i = 0;
        for (let product of this.cart) {
            if (product["product"]["id"] == item["id"]) {
                this.cart.splice(i, 1);

                this.save();
                return;
            }
        	i += 1;
        }

        console.debug("Item not found in cart");
        this.save();
    }
}
