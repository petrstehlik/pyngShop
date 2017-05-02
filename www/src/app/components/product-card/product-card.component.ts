import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import {TruncatePipe} from 'app/utils/truncate.pipe';

@Component({
  selector: 'product-card',
  templateUrl: './product-card.component.html',
  styleUrls: ['./product-card.component.scss']
})
export class ProductCardComponent implements OnInit {

	@Input() item : Object;

	constructor(private router : Router) { }

	ngOnInit() {
		console.log(this.item);
	}

	redirect() {
		this.router.navigate(['product', this.item["id"]]);
	}

}
