import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { ProductService } from 'app/services/product.service';

@Component({
  selector: 'app-product-new',
  templateUrl: './product-new.component.html',
  styleUrls: ['./product-new.component.scss'],
  providers : [ProductService]
})
export class ProductNewComponent implements OnInit {

	productid = null;
	categoryid = null;
	err = null;

	product = {
		image : null,
		price : 0,
		in_stock : 0,
		name : null,
		description : null,
		hidden : false
	}

  constructor(private route: ActivatedRoute,
  			 private router : Router,
  			 private productService : ProductService) { }

	ngOnInit() {
		this.route.params.subscribe(params => {
			//this.productid = +params['productid'];
			this.categoryid = +params['categoryid']
		});
	}

	save() {
		this.product["categories"] = [{"id" : this.categoryid}];
		console.log(this.product);

		this.productService.add(this.product).subscribe(
		data => {
			this.router.navigate(['/', 'products', data["id"]]);
		},
		err => {
			console.log(err);
			this.err = err;
		})
	}

	null(event) {
		return;
	}

}
