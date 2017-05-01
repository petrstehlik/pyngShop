import { Component, OnInit, Input } from '@angular/core';

<<<<<<< HEAD
import { UserService } from 'app/services';
import {CategoryService } from 'app/services/category.service';

@Component({
  selector: 'category-item',
  templateUrl: './category-item.component.html',
  styleUrls: ['./category-item.component.scss'],
  providers : [UserService]
=======
@Component({
  selector: 'category-item',
  templateUrl: './category-item.component.html',
  styleUrls: ['./category-item.component.scss']
>>>>>>> 9107357... Components: Category Bar and Item
})
export class CategoryItemComponent implements OnInit {

    @Input() item : Object;
<<<<<<< HEAD

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
=======
    user = {
        admin: false
    }

  constructor() { }

  ngOnInit() {
      console.log(this.item);
  }
>>>>>>> 9107357... Components: Category Bar and Item

}
