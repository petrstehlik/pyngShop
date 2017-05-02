import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { ProductService } from 'app/services/product.service';
import { UserService } from 'app/services/user.service';
import { CartService } from 'app/services/cart.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss'],
  providers : [ProductService, UserService, CartService]
})
export class ProductComponent implements OnInit {

	product = {};
	quantity = 1;
	id = 0;

	constructor(private route: ActivatedRoute,
               private productService : ProductService,
               private user : UserService,
               private cart : CartService) {}

	ngOnInit() {
		this.route.params.subscribe(params => {
			this.id = +params['id']; // (+) converts string 'id' to a number

            this.getProduct();
        });
	}

	getProduct() {
        this.productService.fetch(this.id).subscribe(
            data => {
                this.product = data;
            },
            error => {
                console.log(error);
            }
        );
    }

    addToCart() {
		this.cart.addItem(this.product, this.quantity);
    }
}
