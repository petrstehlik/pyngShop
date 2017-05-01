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
        return this.cart.length;
    }

    addItem(item : Object) {
        for (let product of this.cart) {
            if (product["product"]["id"] == item["id"]) {
                product["quantity"] += item["quantity"];
                this.save();
                return;
            }
        }

        this.cart.push(item);

        this.save();
    }

    removeItem(item : Object) {
        for (let product of this.cart) {
            if (product["product"]["id"] == item["id"]) {
                product["quantity"] -= item["quantity"];
                this.save();
                return;
            }
        }

        console.debug("Item not found in cart");
    }
}
