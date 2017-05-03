/**
  * http://youknowriad.github.io/angular2-cookbooks/pipe.html
  */

import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'truncate'
})
export class TruncatePipe implements PipeTransform {
	transform(value: string, args: string) : string {
		console.log(value);
		console.log("args", args);
		let limit = parseInt(args, 10);
		let trail = args.length > 1 ? args : '...';

		console.log("limit");
		console.log(parseInt(args, 10));

	  	try {
	  		return value.length > limit ? value.substring(0, limit) + trail : value;
		} catch (e) {
			return "";
		}
	}
}
