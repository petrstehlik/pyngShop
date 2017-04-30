import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule} from '@angular/router';
import { FormsModule }		from '@angular/forms';
//import { HttpService } from '../../services/http.service';
import {
	usersComponent,
	usersAddComponent,
	usersListComponent,
	usersEditComponent
	} from './users.component';

<<<<<<< HEAD
import { TopBarModule } from 'app/components/topbar/top-bar.module';

=======
>>>>>>> e0bddf3... Add base for modules
import { AuthGuard } from  'app/utils/auth.guard';

const usersRoutes : Routes = [
	{
<<<<<<< HEAD
		path : 'admin/users',
=======
		path : 'users',
>>>>>>> e0bddf3... Add base for modules
		component : usersComponent,
		canActivate : [AuthGuard],
		data : {
			basepath : true,
			name : "Users",
			description : "Manage users, update profiles and passwords.",
			icon : "fa-user-circle",
			role : 0
		},
		children : [
			{
				path : '',
				component: usersListComponent,
				canActivate : [AuthGuard],
				data : {
					role : 0
				}
			},
			{
				path : 'add',
				component : usersAddComponent,
				canActivate : [AuthGuard],
				data : {
					role : 0,
					name : 'Add User'
				}
			},
			{
				path : ':id',
				component : usersEditComponent,
				canActivate : [AuthGuard],
				data : {
					role : 0,
					name : 'Edit User'
				}
			}
		]
	}
];

//export const dummyRouting = RouterModule.forChild(dummyRoutes);

@NgModule({
	imports : [
		CommonModule,
		FormsModule,
<<<<<<< HEAD
		TopBarModule,
=======
>>>>>>> e0bddf3... Add base for modules
		RouterModule.forChild(usersRoutes)
	],
	declarations : [usersComponent, usersAddComponent, usersListComponent, usersEditComponent],
	exports : [usersComponent, usersAddComponent, usersEditComponent, RouterModule],
	//	providers : [HttpService]
})
export class usersModule {};
