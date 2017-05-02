import { Component, OnInit } from '@angular/core';
import { OrderService } from 'app/services';

@Component({
  selector: 'app-admin-orders',
  templateUrl: './admin-orders.component.html',
  styleUrls: ['./admin-orders.component.scss'],
  providers : [OrderService]
})
export class AdminOrdersComponent implements OnInit {

	orders = null;

	constructor(private orderService : OrderService) { }

	ngOnInit() {
		this.orderService.fetchAll().subscribe(
			data => {
				this.orders = data;
			},
			err => {
				console.log(err);
			}
		)

	}

}
