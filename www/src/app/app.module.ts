import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http, Request, XHRBackend, RequestOptions} from '@angular/http';
import { RouterModule, Routes, Router } from '@angular/router';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/';
import { LoginComponent } from './components/';
import { LogoutComponent } from './components/';
import { SetupComponent } from './components/';
import { NullComponent, TopBarComponent } from './components/';
import { CustomerLoginComponent } from './components/customer-login/login.component';


import { AuthGuard } from './utils/index';
import { HttpInterceptor } from './utils/index';
import { SafePipe, SafePipeModule } from 'app/utils/safe.pipe';

import { modules } from './modules';
import { CategoryBarComponent } from './components/category-bar/category-bar.component';
import { CategoryItemComponent } from './components/category-item/category-item.component';
import { CategoryComponent } from './components/category/category.component';

import {UserService} from './services/user.service'

import {InlineEditorModule} from 'ng2-inline-editor';

export const appRoutes: Routes = [
	{
		path : 'admin/login',
		component : LoginComponent
	},
	{
		path : 'login',
		component : CustomerLoginComponent
	},
	{
		path : 'logout',
		component : LogoutComponent,
		canActivate : [AuthGuard]
	},
    {
        path : 'category/:id',
        component : CategoryComponent
    },
	{
		path: '',
		component: HomeComponent,
		canActivate : []
	},
	{
		path: '**',
		component: NullComponent
	}
];

export function setFactory (xhrBackend: XHRBackend,
				requestOptions: RequestOptions,
				router: Router) {
	return new HttpInterceptor(xhrBackend, requestOptions, router);
}

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    CustomerLoginComponent,
    LogoutComponent,
    SetupComponent,
    NullComponent,
    TopBarComponent,
    CategoryBarComponent,
    CategoryItemComponent,
    CategoryComponent
  ],
  imports: [
	modules,
	SafePipeModule,
    BrowserModule,
	FormsModule,
	HttpModule,
	InlineEditorModule,
	NgbModule.forRoot(),
	RouterModule.forRoot(appRoutes)
  ],
  providers: [
	AuthGuard,
	UserService,
	SafePipe,
		{
			provide : Http,
			useFactory: setFactory,
			deps: [XHRBackend, RequestOptions, Router]
		}

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
