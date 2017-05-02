import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { OrderService} from 'app/services';

@Component({
  selector: 'app-admin-order-detail',
  templateUrl: './admin-order-detail.component.html',
  styleUrls: ['./admin-order-detail.component.scss'],
  providers : [OrderService]
})
export class AdminOrderDetailComponent implements OnInit {

	id;
	order;
	total = 0;

  constructor(private route: ActivatedRoute,
  			 private orderService : OrderService) { }

  ngOnInit() {
  	  this.route.params.subscribe(params => {
            this.id = +params['id']; // (+) converts string 'id' to a number

            this.getOrder();

            // In a real app: dispatch action to load the details here.
        });
  }

  getOrder() {
  	  this.orderService.fetch(this.id).subscribe(
		data => {
			this.order = data;
			this.getTotal();
		},
		err => {
			console.log(err);
		}
  	  );
  }

  update() {
          this.orderService.update(this.order).subscribe(
              data => {
                  this.order = data;
              },
              err => {
                  console.log(err);
              }
          );
      }


      getTotal() {
		this.total = 0;

		for (let item of this.order["ordered_products"]) {
			this.total += item["product"]["price"] * item["quantity"];
		}

		/*for (let item of this.shipping) {
			if (item["id"] == this.selectedShipping) {
				this.total += item["price"];
			}
		}*/

	}


}
