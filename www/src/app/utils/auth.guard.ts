import { Injectable } from '@angular/core';
import { CanActivate, Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  CanActivateChild,
  NavigationExtras,
  CanLoad, Route } from '@angular/router';

@Injectable()
export class AuthGuard implements CanActivate, CanLoad {

	constructor(private router: Router) { }

	isLoggedIn() : boolean {
	    if (localStorage.getItem('currentUser')) {
            // logged in so return true
            return true;
        }

        // not logged in so redirect to login page with the return url
        return false;
	}

	canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
		let user = JSON.parse(localStorage.getItem('currentUser'));
        if (this.isLoggedIn()) {
		// logged in so return true
		//console.log(route.data)
			if (route.data['role'] == undefined) {
				console.warn('No role is set for route \'' + route.data['path'] + '\'');
				return true;
			}

			if (user.user.role <= route.data['role']) {
				return true;
			}

			console.warn('User is not allowed to access \'' + route.data['path'] + '\'')
			return false;
        }

		if (route.data['role'] == 0)
			this.router.navigate(['/admin/login'], { queryParams: { returnUrl: state.url }});
		else
        // not logged in so redirect to login page with the return url
        	this.router.navigate(['/login'], { queryParams: { returnUrl: state.url }});
        return false;
	}

	canLoad(route : Route) : boolean {
		if (this.isLoggedIn()) {
			return true;
		}
		return false;
	}
}
