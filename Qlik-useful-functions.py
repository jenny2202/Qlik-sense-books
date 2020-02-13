# Qlik useful functions:
Using an extended interval match to handle Slowly Changing Dimensions
Using the Previous() function to identify the latest record for a dimensional value
Using the NetworkDays() function to calculate the working days in a calendar month
Using the Concat() function to display a string of field values as a dimension
Using the MinString() function to calculate the age of the oldest case in a queue f Using the RangeSum() function to plot cumulative figures in trendline charts
Using the Fractile() function to generate quartiles
Using the FirstSortedValue() function to identify the median in a quartile range f Using the Derive and Declare functions to generate Calendar fields
Setting up a moving annual total figure
Using the For Each loop to extract files from a folder
Using the Peek() function to create a currency Exchange Rate Calendar
Using the Peek()function to create a Trial Balance sheet


# Percentage
(Sum(Sales)-Sum(Target))/Sum(Target)

# Highlight color
 If(Sum({<Year={2014}>}Sales)>Sum({<Year={2015}>}Sales),
         Red(),Green())

or:

If((Sum({<Year={2015}>}Sales)-
   Sum({<Year={2014}>}Sales))/Sum({<Year={2015}>}Sales)>0,
   ColorMix1((Sum({<Year={2015}>}Sales)-
   Sum({<Year={2014}>}Sales))/Sum({<Year={2015}>}Sales),
   white(),RGB(50,255,50)), if((Sum({<Year={2015}>}Sales)-
   Sum({<Year={2014}>}Sales))/Sum({<Year={2015}>}Sales)<0,
   ColorMix1(fabs((Sum({<Year={2015}>}Sales)-
   Sum({<Year={2014}>}Sales))/Sum({<Year={2015}>}Sales)),
   white(),RGB(255,50,50))))


# Upper/lower threshold line to Reference line
Avg(BounceRate)+Stdev(Total Aggr( Avg(BounceRate),Period))

Avg(BounceRate)-Stdev(Total Aggr( Avg(BounceRate),Period))


# Average of data with outliers removed
Avg(If (Calls > Aggr(NODISTINCT Fractile(Calls, 0.1),
         Month) and Calls < Aggr(NODISTINCT Fractile(Calls, 0.9),
         Month),Calls))


# Calculate number of working days
 LOAD *,
       Month(PostingDate) as Month,
       MonthName(PostingDate) AS MonthYear,
       IF(Year(PostingDate)=Year(TODAY()) AND Month(PostingDate)=MONTH(TO
       DAY()),
         NETWORKDAYS(MONTHSTART(today()),(Today()),
         $(vPublicHolidays)), NETWORKDAYS(MONTHSTART(PostingDate),
         MonthEnd(PostingDate),
       $(vPublicHolidays))) AS WorkingDays RESIDENT
       SalesTmp;
       DROP table SalesTmp;
         DROP table HolidayTmp;


# Using concat() to display a string of field values as a dimension
AGGR(Concat(DISTINCT Product,','),OrderID)
-- The Concat() function can also be used in the script along with the Group By clause.
# Using the Fractile() function to generate quartiles


# Using the Minstring() to calculate the age of the oldest case(item) in a queue
LET vToday=num(today()) -- setting variable
Num($(vToday)-(MinString({$<DateLogged=>}
     [DateLogged])),'#,##0')


# Fractile() to generate quartiles
=If (Value <= Fractile (TOTAL Value, 0.25), 'Quartile 1',
    If (Value <= Fractile (TOTAL Value, 0.50), 'Quartile 2',
    If (Value <= Fractile (TOTAL Value, 0.75),'Quartile 3',
    'Quartile 4')))


# FirstSortedValue() to identify the median in quartile range
 if(Match(CaseID,
   '$(=FirstSortedValue(distinct{<Value={"<=$(=Median({<Value=
     {'>=$(=fractile(Value, 0))<=$(=Fractile(Value, 0.25))'}>}
     Value))"}>} CaseID, -Value))',
   '$(=FirstSortedValue(distinct{<Value={"<=$(=Median({<Value=
     {'>$(=fractile(Value, 0.25))<=$(=fractile(Value,
     0.5))'}>} Value))"}>} CaseID, -Value))',
   '$(=FirstSortedValue(distinct{<Value={"<=$(=Median({<Value=
     {'>$(=fractile(Value, 0.5))<=$(=fractile(Value,
     0.75))'}>} Value))"}>} CaseID, -Value))',
   '$(=FirstSortedValue(distinct{<Value={"<=$(=Median({<Value=
     {'>$(=fractile(Value, 0.75))<=$(=fractile(Value, 1))'}>}
     Value))"}>} CaseID, -Value))'
   ),
   CaseID,
   Null()
   )


# Declare and Derive functions
 Calendar:
       Declare Field Definition Tagged '$date'
       Parameters
           first_month_of_year=1
        Fields
              Year($1)  as Year Tagged '$year',
               Month($1) as Month Tagged '$month',
               Date($1) as Date Tagged '$date',
               Week($1,first_month_of_year) as Week Tagged '$week'
           Groups
           Year,Month,Date type collection as YearMonthDate;

Derive Fields from Fields InvoiceDate using Calendar;

# MAT Month year function page 147 for showing 12 months


# compare the current year versus last year sales for three countries, 
# we can write the following Set Analysis expression:

Sum({$<Year={2014,2015},Country={'USA', 'UK', 'GERMANY'}>}Sales)


Sum({$<Volume ={">=200"}>} Sales)

Sum({$<Month=,Volume ={">=200"}>} Sales)

## Adding new field with calculations
SaleTemp1:
LOAD * ,
   IF(num(DeliveryDate)-num(ShipmentDate)>=0 AND
   Num(DeliveryDate)-num(ShipmentDate)<5 ,1,
   IF(num(DeliveryDate)-num(ShipmentDate)>=5 AND
   Num(DeliveryDate)-num(ShipmentDate)<25 ,2,3)) AS
     OntimeLateFlag
   RESIDENT SalesTemp;
   DROP TABLE SalesTemp;

Sales:
       LOAD *,
       IF(OntimeLateFlag =1, Dual('OnTime',1),
       IF(OntimeLateFlag =2, Dual('SlightDelay',2),
         Dual('Late',3))) As Flag
       RESIDENT SalesTemp1;
       DROP Table SalesTemp1;


### Page 171 - Using comparison sets in Set Analysis
### Page 175 - Multiple measures expression

#### Page 182 A P() function returns a set of all possible values while an E() function returns a set of all excluded values.

