
export const useDateArray = (dateInput: Date) => {

    const monthNames:string[] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    var dateArray:Date[] = [];

    for(var i=1; i <= 24; i++) {
        const dateForArray:Date = new Date(dateInput.getFullYear(), dateInput.getMonth() + i,0,0,0,0,0);
        dateArray.push(dateForArray);
    }

    var dateNamesArray:string[] = [];

    for(var i=0; i < dateArray.length; i++) {

        const month:string = monthNames[dateArray[i].getMonth()];
        const year:string = dateArray[i].getFullYear().toString()[2] + dateArray[i].getFullYear().toString()[3];
        console.log(year);
        const arrayInput:string = month + " " + year;
        dateNamesArray.push(arrayInput);

    }

    return dateNamesArray;

}