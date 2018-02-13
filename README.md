# donation-analytics
donation analytics challenge problem

https://github.com/InsightDataScience/donation-analytics/blob/master/README.md

* to solve the problem, first a record has to be identified as a repeat donor, then, if it is, a percentile needs to be calculated using the amounts of other records with matching CMTE_IDs, zip codes and years.
* For each record, you need to search the prior records for other records that match these parameters.
* But saving all the lines that come in so that you can search them would take a lot of space. Instead, I use two hash maps and a binary tree to store the information coming in so that when a percentile needs to be calculated, it can be done quickly.
* The name and zip code are mapped to a year in the first hash map, so that a repeat donor can be quickly identified when it is streamed in. 
* Then, the zip, year and CMTE_ID and amount are added to a zip-year-cmte to amount-list hash map. And the list of amounts are returned to calculate the percentile.
* finally, in order to calculate the percentile from the amounts, they need to be ordered. To speed up the ordering proceess, the list of amounts in the hashmap is actually stored as a binary tree, so that they are already ordered. This is faster than sorting the list each time when needing to caclulate the percentile. 
* The hash maps are O(1) and creating and finding and element in the binary tree are worst case O(n)