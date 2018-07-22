# Getting data with Hap!
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.


## How to gather data with Hap
- Install Python package `hap`
- Make new folder `/tmp/testing_hap`;
- Go to `/tmp/testing_hap`;
- Create new file `shop.json`;
- Add the following content to file `shop.json`:
```
{
    "declare": {
        "product_link": "string",
        "product_name": "string",
        "product_price": "decimal",
        "product_currency": "string"
    },
    "define": [
        {
            "product_link": [
                {
                    "query_xpath": "//*[@itemprop='url']/text()"
                }
            ]
        },
        {
            "product_name": [
                {
                    "query_xpath": "//*[@itemprop='name']/text()"
                }
            ]
        },
        {
            "product_price": [
                {
                    "query_xpath": "//*[@itemprop='price']/@content"
                },
                {
                    "remove": "[^,\\.\\d]"
                }
            ]
        },
        {
            "product_price": [
                {
                    "query_xpath": "//*[@itemprop='price']/text()"
                },
                {
                    "remove": "[^,\\.\\d]"
                }
            ]
        },
        {
            "product_currency": [
                {
                    "query_xpath": "//*[@itemprop='priceCurrency']/@content"
                }
            ]
        },
        {
            "product_currency": [
                {
                    "query_xpath": "//*[@itemprop='priceCurrency']/text()"
                }
            ]
        }
    ]
}
```

- Run `hap shop.json --save --verbose --link <shop_url>`;
- List everything.
