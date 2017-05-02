import { Component, OnInit } from '@angular/core';
import { AdminShippingService } from 'app/services';


export class Shipping {
	constructor(
	public name : string,
	public price: number
	) { }
}

@Component({
  selector: 'app-admin-shipping',
  templateUrl: './admin-shipping.component.html',
  styleUrls: ['./admin-shipping.component.scss'],
  providers : [AdminShippingService]
})
export class AdminShippingComponent implements OnInit {
	shippingList = [];
	shipping = new Shipping('', 0);
	submitted = false;
	editMode = false;
	editShip = null;

	constructor( private shippingService : AdminShippingService) { }

	ngOnInit() {
	this.fetchAll();
	}

	edit(sh) {
		this.editMode = true;
		this.editShip = sh;
	}

	save() {
		this.shippingService.update(this.editShip["id"], this.editShip)
			.subscribe(
				data => {
					this.fetchAll();
					this.editMode = false;
					this.editShip = null;
				},
				err => {
					console.debug("save");
					console.log(err);
				});
	}

	remove(sh) {
		this.shippingService.remove(sh["id"])
			.subscribe(
				data => {
					this.fetchAll();
				},
				err => {
					console.debug("Remove");
					console.log(err);
				});
	}


	fetchAll() {
		this.shippingService.fetchAll()
			.subscribe(
				data => {
					this.shippingList = data;
				},
				err => {
					console.debug("FetchAll");
					console.log(err);
				});
	}

	add() {
		this.submitted = true;
		this.shippingService.add(this.shipping)
			.subscribe(
				data => {
					this.shippingList.push(data);
					this.shipping = new Shipping('', 0);
				},
				err => {
					console.log(err);
				});
	}

}
