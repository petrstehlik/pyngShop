import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-product-new',
  templateUrl: './product-new.component.html',
  styleUrls: ['./product-new.component.scss']
})
export class ProductNewComponent implements OnInit {

	productid = null;
	categoryid = null;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
  	  this.route.params.subscribe(params => {
            this.productid = +params['productid'];
            this.categoryid = +params['categoryid']

        });
  }

}
