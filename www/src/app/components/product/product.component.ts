import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { ProductService } from 'app/services/product.service';
import { UserService } from 'app/services/user.service';
import { CartService } from 'app/services/cart.service';
import { ReviewService } from 'app/services/review.service';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss'],
  providers : [ProductService, UserService, CartService, ReviewService]
})
export class ProductComponent implements OnInit {

	product = {};
	quantity = 1;
	id = 0;
	submitted = false;
	message = null;
	newReview = {
		rating : 0,
		content : ""
	}

	reviews;

	constructor(private route: ActivatedRoute,
               private productService : ProductService,
               private user : UserService,
               private cart : CartService,
               private review : ReviewService) {}

	ngOnInit() {
		this.route.params.subscribe(params => {
			this.id = +params['id']; // (+) converts string 'id' to a number

            this.getProduct();
            this.getReviews();
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

   update(event) {
     this.submitted = true;
     this.message = null;
     this.productService.update(this.product).subscribe(
       data => {
         this.product = data;
         this.message = "Update successfull";
       },
       error => {
         console.log(error);
         this.message = error["message"];
         this.submitted = false;
       }
      );
   }

   remove() {
     this.submitted = true;
     this.message = null;
     this.product["hidden"] = !this.product["hidden"];
     this.productService.update(this.product).subscribe(
       data => {
         this.product = data;
         this.message = "Update successfull";
       },
       error => {
         console.log(error);
         this.message = error["message"];
         this.submitted = false;
       }
      );
   }

    addToCart() {
		this.cart.addItem(this.product, this.quantity);
    }

    addReview() {
		console.log(this.newReview);

		this.review.add(this.id, this.newReview).subscribe(
			data => {
				this.getReviews();
				this.newReview = {
					rating : null,
					content : ""
				};
				this.message = {"error" : false, "message" : "Review added successfully"};
			},
			err => {
				this.message = {error: true, "message" : "Failed to add review, you cannot add two reviews."};
			}
		)
    }

    getReviews() {
		this.review.fetch(this.id).subscribe(
			data => {
				this.reviews = data;
			},
			err => {
				this.message = {error: true, "message" : "Failed to add review, you cannot add two reviews."};
			}
		)
    }

    checkQuantity(event) {
    	console.log(event);
    	if (event > this.product["in_stock"]) {
    		this.quantity = this.product["in_stock"];
    		return this.quantity;
		}

    	if (event < 1)
    		this.quantity = 1;
    		return this.quantity;
    }
}
