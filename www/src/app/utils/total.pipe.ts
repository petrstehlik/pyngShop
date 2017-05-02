import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'total'
})

export class TotalPipe implements PipeTransform {
	transform(value: Array<Object>, args: string[]) : Number {
		let total = 0;
		for (let item of value) {
			total += item["product"]["price"] * item["quantity"];
		}

	  	return total;
	}
}

