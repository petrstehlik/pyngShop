import { Component, OnInit, Input } from '@angular/core';

import { UserService } from 'app/services';
import {CategoryService } from 'app/services/category.service';

@Component({
  selector: 'category-item',
  templateUrl: './category-item.component.html',
  styleUrls: ['./category-item.component.scss'],
  providers : [UserService]
})
export class CategoryItemComponent implements OnInit {

    @Input() item : Object;

    edit_enabled = false;

    constructor(private user : UserService,
    		   private category : CategoryService) { }

    ngOnInit() {
    }

    deleteCategory(id : Number) {
		this.category.delete(this.item["id"]).subscribe(
			data => {
				this.item["hidden"] = true;
			},
			error => {
				console.log(error);
			}
		);
    }

}
