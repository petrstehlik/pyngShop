import { Component, OnInit } from '@angular/core';

import { StatsService } from 'app/services/stats.service';
import { CategoryService } from 'app/services/category.service';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
  providers : [StatsService, CategoryService]
})
export class AdminComponent implements OnInit {

	products;
	orders;

	constructor(private stats : StatsService) { }

	ngOnInit() {
		this.stats.products().subscribe(
			data => {
				this.products = data;
			},
			err => {
				console.log(err);
			}
		);

		this.stats.orders().subscribe(
			data => {
				this.orders = data;
			},
			err => {
				console.log(err);
			}
		);

	}

}
