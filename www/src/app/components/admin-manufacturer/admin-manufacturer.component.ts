import { Component, OnInit } from '@angular/core';
import { AdminManufacturerService } from 'app/services';
import { Manufacturer} from 'app/components/manufacturer/manufacturer.component';

@Component({
	selector: 'app-admin-manufacturer',
	templateUrl: './admin-manufacturer.component.html',
	styleUrls: ['./admin-manufacturer.component.scss'],
	providers : [AdminManufacturerService]
})
export class AdminManufacturerComponent implements OnInit {
	manufacturer = new Manufacturer('', '', '', +420, '', 0, 0);
	manufacturers = [];
	submitted = false;
	editMode = false;
	editMan = null;

	constructor( private manufacturerService : AdminManufacturerService) { }

	ngOnInit() {
		this.fetchAll();
	}

	edit(man) {
		this.editMode = true;
		this.editMan = man;
	}

	save(man) {
		this.manufacturerService.update(man["id"], man)
			.subscribe(
				data => {
					this.fetchAll();
					this.editMode = false;
					this.editMan = null;
				},
				err => {
					console.debug("save");
					console.log(err);
				});
	}

	remove(man) {
		this.manufacturerService.remove(man["id"])
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
		this.manufacturerService.fetchAll()
			.subscribe(
				data => {
					this.manufacturers = data;
				},
				err => {
					console.debug("FetchAll");
					console.log(err);
				});
	}

	add() {
		this.submitted = true;
		this.manufacturerService.add(this.manufacturer)
			.subscribe(
				data => {
					this.manufacturers.push(data);
					this.manufacturer = new Manufacturer('', '', '', +420, '', 0, 0);
				},
				err => {
					console.log(err);
				});
	}

}
