# -*- coding: utf-8 -*-
import scrapy
import json
from urllib import urlencode
import time

_search_info = r"""{"provence":[{"bj":"\u5317\u4eac"},{"tj":"\u5929\u6d25"},{"sh":"\u4e0a\u6d77"},{"cq":"\u91cd\u5e86"},{"heb":"\u6cb3\u5317"},{"sx":"\u5c71\u897f"},{"nmg":"\u5185\u8499\u53e4"},{"ln":"\u8fbd\u5b81"},{"jl":"\u5409\u6797"},{"hlj":"\u9ed1\u9f99\u6c5f"},{"js":"\u6c5f\u82cf"},{"zj":"\u6d59\u6c5f"},{"ah":"\u5b89\u5fbd"},{"fj":"\u798f\u5efa"},{"jx":"\u6c5f\u897f"},{"sd":"\u5c71\u4e1c"},{"hen":"\u6cb3\u5357"},{"hub":"\u6e56\u5317"},{"hun":"\u6e56\u5357"},{"gd":"\u5e7f\u4e1c"},{"gx":"\u5e7f\u897f"},{"han":"\u6d77\u5357"},{"sc":"\u56db\u5ddd"},{"gz":"\u8d35\u5dde"},{"yn":"\u4e91\u5357"},{"xz":"\u897f\u85cf"},{"snx":"\u9655\u897f"},{"gs":"\u7518\u8083"},{"qh":"\u9752\u6d77"},{"nx":"\u5b81\u590f"},{"xj":"\u65b0\u7586"}],"city":{"zonj":["\u603b\u5c40"],"bj":["\u5317\u4eac\u5e02"],"tj":["\u5929\u6d25\u5e02"],"sh":["\u4e0a\u6d77\u5e02"],"cq":["\u91cd\u5e86\u5e02"],"heb":["\u5168\u90e8","\u77f3\u5bb6\u5e84","\u5510\u5c71","\u79e6\u7687\u5c9b","\u90af\u90f8","\u90a2\u53f0","\u4fdd\u5b9a","\u5f20\u5bb6\u53e3","\u627f\u5fb7","\u6ca7\u5dde","\u5eca\u574a","\u8861\u6c34"],"sx":["\u5168\u90e8","\u592a\u539f","\u5927\u540c","\u9633\u6cc9","\u957f\u6cbb","\u664b\u57ce","\u6714\u5dde","\u664b\u4e2d","\u8fd0\u57ce","\u5ffb\u5dde","\u4e34\u6c7e","\u5415\u6881"],"nmg":["\u5168\u90e8","\u547c\u548c\u6d69\u7279","\u5305\u5934","\u4e4c\u6d77","\u8d64\u5cf0","\u901a\u8fbd","\u9102\u5c14\u591a\u65af","\u547c\u4f26\u8d1d\u5c14","\u5df4\u5f66\u6dd6\u5c14","\u4e4c\u5170\u5bdf\u5e03","\u5174\u5b89\u76df","\u9521\u6797\u90ed\u52d2\u76df","\u963f\u62c9\u5584\u76df"],"ln":["\u5168\u90e8","\u6c88\u9633","\u5927\u8fde","\u978d\u5c71","\u629a\u987a","\u672c\u6eaa","\u4e39\u4e1c","\u9526\u5dde","\u8425\u53e3","\u961c\u65b0","\u8fbd\u9633","\u76d8\u9526","\u94c1\u5cad","\u671d\u9633","\u846b\u82a6\u5c9b"],"jl":["\u5168\u90e8","\u957f\u6625","\u5409\u6797","\u56db\u5e73","\u8fbd\u6e90","\u901a\u5316","\u767d\u5c71","\u677e\u539f","\u767d\u57ce","\u5ef6\u8fb9\u671d\u9c9c\u65cf\u81ea\u6cbb\u5dde"],"hlj":["\u5168\u90e8","\u54c8\u5c14\u6ee8","\u9f50\u9f50\u54c8\u5c14","\u9e21\u897f","\u9e64\u5c97","\u53cc\u9e2d\u5c71","\u5927\u5e86","\u4f0a\u6625","\u4f73\u6728\u65af","\u4e03\u53f0\u6cb3","\u7261\u4e39\u6c5f","\u9ed1\u6cb3","\u7ee5\u5316","\u5927\u5174\u5b89\u5cad\u5730\u533a"],"js":["\u5168\u90e8","\u5357\u4eac","\u65e0\u9521","\u5f90\u5dde","\u5e38\u5dde","\u82cf\u5dde","\u5357\u901a","\u8fde\u4e91\u6e2f","\u6dee\u5b89","\u76d0\u57ce","\u626c\u5dde","\u9547\u6c5f","\u6cf0\u5dde","\u5bbf\u8fc1"],"zj":["\u5168\u90e8","\u676d\u5dde","\u5b81\u6ce2","\u6e29\u5dde","\u5609\u5174","\u6e56\u5dde","\u7ecd\u5174","\u91d1\u534e","\u8862\u5dde","\u821f\u5c71","\u53f0\u5dde","\u4e3d\u6c34"],"ah":["\u5168\u90e8","\u5408\u80a5","\u829c\u6e56","\u868c\u57e0","\u6dee\u5357","\u9a6c\u978d\u5c71","\u6dee\u5317","\u94dc\u9675","\u5b89\u5e86","\u9ec4\u5c71","\u6ec1\u5dde","\u961c\u9633","\u5bbf\u5dde","\u516d\u5b89","\u4eb3\u5dde","\u6c60\u5dde","\u5ba3\u57ce"],"fj":["\u5168\u90e8","\u798f\u5dde","\u53a6\u95e8","\u8386\u7530","\u4e09\u660e","\u6cc9\u5dde","\u6f33\u5dde","\u5357\u5e73","\u9f99\u5ca9","\u5b81\u5fb7"],"jx":["\u5168\u90e8","\u5357\u660c","\u666f\u5fb7\u9547","\u840d\u4e61","\u4e5d\u6c5f","\u65b0\u4f59","\u9e70\u6f6d","\u8d63\u5dde","\u5409\u5b89","\u5b9c\u6625","\u629a\u5dde","\u4e0a\u9976"],"sd":["\u5168\u90e8","\u6d4e\u5357","\u9752\u5c9b","\u6dc4\u535a","\u67a3\u5e84","\u4e1c\u8425","\u70df\u53f0","\u6f4d\u574a","\u6d4e\u5b81","\u6cf0\u5b89","\u5a01\u6d77","\u65e5\u7167","\u83b1\u829c","\u4e34\u6c82","\u5fb7\u5dde","\u804a\u57ce","\u6ee8\u5dde","\u83cf\u6cfd"],"hen":["\u5168\u90e8","\u90d1\u5dde","\u5f00\u5c01","\u6d1b\u9633","\u5e73\u9876\u5c71","\u5b89\u9633","\u9e64\u58c1","\u65b0\u4e61","\u7126\u4f5c","\u6fee\u9633","\u8bb8\u660c","\u6f2f\u6cb3","\u4e09\u95e8\u5ce1","\u5357\u9633","\u5546\u4e18","\u4fe1\u9633","\u5468\u53e3","\u9a7b\u9a6c\u5e97","\u7701\u76f4\u8f96\u53bf\u7ea7\u884c\u653f\u533a\u5212"],"hub":["\u5168\u90e8","\u6b66\u6c49","\u9ec4\u77f3","\u5341\u5830","\u5b9c\u660c","\u8944\u9633","\u9102\u5dde","\u8346\u95e8","\u5b5d\u611f","\u8346\u5dde","\u9ec4\u5188","\u54b8\u5b81","\u968f\u5dde","\u6069\u65bd\u571f\u5bb6\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde","\u7701\u76f4\u8f96\u53bf\u7ea7\u884c\u653f\u533a\u5212"],"hun":["\u5168\u90e8","\u957f\u6c99","\u682a\u6d32","\u6e58\u6f6d","\u8861\u9633","\u90b5\u9633","\u5cb3\u9633","\u5e38\u5fb7","\u5f20\u5bb6\u754c","\u76ca\u9633","\u90f4\u5dde","\u6c38\u5dde","\u6000\u5316","\u5a04\u5e95","\u6e58\u897f\u571f\u5bb6\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde"],"gd":["\u5168\u90e8","\u4e1c\u839e","\u4e2d\u5c71","\u5e7f\u5dde","\u97f6\u5173","\u6df1\u5733","\u73e0\u6d77","\u6c55\u5934","\u4f5b\u5c71","\u6c5f\u95e8","\u6e5b\u6c5f","\u8302\u540d","\u8087\u5e86","\u60e0\u5dde","\u6885\u5dde","\u6c55\u5c3e","\u6cb3\u6e90","\u9633\u6c5f","\u6e05\u8fdc","\u6f6e\u5dde","\u63ed\u9633","\u4e91\u6d6e"],"gx":["\u5168\u90e8","\u5357\u5b81","\u67f3\u5dde","\u6842\u6797","\u68a7\u5dde","\u5317\u6d77","\u9632\u57ce\u6e2f","\u94a6\u5dde","\u8d35\u6e2f","\u7389\u6797","\u767e\u8272","\u8d3a\u5dde","\u6cb3\u6c60","\u6765\u5bbe","\u5d07\u5de6"],"han":["\u5168\u90e8","\u6d77\u53e3","\u4e09\u4e9a","\u7701\u76f4\u8f96\u53bf\u7ea7\u884c\u653f\u533a\u5212"],"sc":["\u5168\u90e8","\u6210\u90fd","\u81ea\u8d21","\u6500\u679d\u82b1","\u6cf8\u5dde","\u5fb7\u9633","\u7ef5\u9633","\u5e7f\u5143","\u9042\u5b81","\u5185\u6c5f","\u4e50\u5c71","\u5357\u5145","\u7709\u5c71","\u5b9c\u5bbe","\u5e7f\u5b89","\u8fbe\u5dde","\u96c5\u5b89","\u5df4\u4e2d","\u8d44\u9633","\u963f\u575d\u85cf\u65cf\u7f8c\u65cf\u81ea\u6cbb\u5dde","\u7518\u5b5c\u85cf\u65cf\u81ea\u6cbb\u5dde","\u51c9\u5c71\u5f5d\u65cf\u81ea\u6cbb\u5dde"],"gz":["\u5168\u90e8","\u8d35\u9633","\u516d\u76d8\u6c34","\u9075\u4e49","\u5b89\u987a","\u6bd5\u8282","\u94dc\u4ec1","\u9ed4\u897f\u5357\u5e03\u4f9d\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde","\u9ed4\u4e1c\u5357\u5dde","\u9ed4\u5357\u5e03\u4f9d\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde"],"yn":["\u5168\u90e8","\u6606\u660e","\u66f2\u9756","\u7389\u6eaa","\u4fdd\u5c71","\u662d\u901a","\u4e3d\u6c5f","\u666e\u6d31","\u4e34\u6ca7","\u695a\u96c4\u5f5d\u65cf\u81ea\u6cbb\u5dde","\u7ea2\u6cb3\u54c8\u5c3c\u65cf\u5f5d\u65cf\u81ea\u6cbb\u5dde","\u6587\u5c71\u58ee\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde","\u897f\u53cc\u7248\u7eb3\u50a3\u65cf\u81ea\u6cbb\u5dde","\u5927\u7406\u767d\u65cf\u81ea\u6cbb\u5dde","\u5fb7\u5b8f\u50a3\u65cf\u666f\u9887\u65cf\u81ea\u6cbb\u5dde","\u6012\u6c5f\u5088\u50f3\u65cf\u81ea\u6cbb\u5dde","\u8fea\u5e86\u85cf\u65cf\u81ea\u6cbb\u5dde"],"xz":["\u5168\u90e8","\u62c9\u8428","\u65e5\u5580\u5219","\u660c\u90fd\u5730\u533a","\u5c71\u5357\u5730\u533a","\u90a3\u66f2\u5730\u533a","\u963f\u91cc\u5730\u533a","\u6797\u829d\u5730\u533a"],"snx":["\u5168\u90e8","\u897f\u5b89","\u94dc\u5ddd","\u5b9d\u9e21","\u54b8\u9633","\u6e2d\u5357","\u5ef6\u5b89","\u6c49\u4e2d","\u6986\u6797","\u5b89\u5eb7","\u5546\u6d1b"],"gs":["\u5168\u90e8","\u5609\u5cea\u5173","\u5170\u5dde","\u91d1\u660c","\u767d\u94f6","\u5929\u6c34","\u6b66\u5a01","\u5f20\u6396","\u5e73\u51c9","\u9152\u6cc9","\u5e86\u9633","\u5b9a\u897f","\u9647\u5357","\u4e34\u590f\u56de\u65cf\u81ea\u6cbb\u5dde","\u7518\u5357\u85cf\u65cf\u81ea\u6cbb\u5dde"],"qh":["\u5168\u90e8","\u897f\u5b81","\u6d77\u4e1c","\u6d77\u5317\u85cf\u65cf\u81ea\u6cbb\u5dde","\u9ec4\u5357\u85cf\u65cf\u81ea\u6cbb\u5dde","\u6d77\u5357\u85cf\u65cf\u81ea\u6cbb\u5dde","\u679c\u6d1b\u85cf\u65cf\u81ea\u6cbb\u5dde","\u7389\u6811\u85cf\u65cf\u81ea\u6cbb\u5dde","\u6d77\u897f\u8499\u53e4\u65cf\u85cf\u65cf\u81ea\u6cbb\u5dde"],"nx":["\u5168\u90e8","\u94f6\u5ddd","\u77f3\u5634\u5c71","\u5434\u5fe0","\u56fa\u539f","\u4e2d\u536b"],"xj":["\u5168\u90e8","\u4e4c\u9c81\u6728\u9f50","\u514b\u62c9\u739b\u4f9d","\u5410\u9c81\u756a\u5730\u533a","\u54c8\u5bc6\u5730\u533a","\u660c\u5409\u56de\u65cf\u81ea\u6cbb\u5dde","\u535a\u5c14\u5854\u62c9\u8499\u53e4\u81ea\u6cbb\u5dde","\u5df4\u97f3\u90ed\u695e\u8499\u53e4\u81ea\u6cbb\u5dde","\u963f\u514b\u82cf\u5730\u533a","\u514b\u5b5c\u52d2\u82cf\u67ef\u5c14\u514b\u5b5c\u81ea\u6cbb\u5dde","\u5580\u4ec0\u5730\u533a","\u548c\u7530\u5730\u533a","\u4f0a\u7281\u54c8\u8428\u514b\u81ea\u6cbb\u5dde","\u5854\u57ce\u5730\u533a","\u963f\u52d2\u6cf0\u5730\u533a","\u81ea\u6cbb\u533a\u76f4\u8f96\u53bf\u7ea7\u884c\u653f\u533a\u5212"]},"industry":[{"priminducode":"","seclist":[{"secnduname":"\u5168\u90e8","secinducode":""}],"priminduname":"\u4e0d\u9650"},{"priminducode":"19","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"19"},{"secnduname":"\u5546\u52a1\u670d\u52a1\u4e1a","secinducode":"1901"},{"secnduname":"\u79df\u8d41\u4e1a","secinducode":"1900"}],"priminduname":"\u79df\u8d41\u548c\u5546\u52a1\u670d\u52a1\u4e1a"},{"priminducode":"17","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"17"},{"secnduname":"\u516c\u5171\u8bbe\u65bd\u7ba1\u7406\u4e1a","secinducode":"1702"},{"secnduname":"\u751f\u6001\u4fdd\u62a4\u548c\u73af\u5883\u6cbb\u7406\u4e1a","secinducode":"1700"}],"priminduname":"\u6c34\u5229\u3001\u73af\u5883\u548c\u516c\u5171\u8bbe\u65bd\u7ba1\u7406\u4e1a"},{"priminducode":"16","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"16"},{"secnduname":"\u9ed1\u8272\u91d1\u5c5e\u77ff\u91c7\u9009\u4e1a","secinducode":"1606"},{"secnduname":"\u7164\u70ad\u5f00\u91c7\u548c\u6d17\u9009\u4e1a","secinducode":"1605"},{"secnduname":"\u975e\u91d1\u5c5e\u77ff\u91c7\u9009\u4e1a","secinducode":"1603"},{"secnduname":"\u6709\u8272\u91d1\u5c5e\u77ff\u91c7\u9009\u4e1a","secinducode":"1601"}],"priminduname":"\u91c7\u77ff\u4e1a"},{"priminducode":"15","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"15"},{"secnduname":"\u96f6\u552e\u4e1a","secinducode":"1501"},{"secnduname":"\u6279\u53d1\u4e1a","secinducode":"1500"}],"priminduname":"\u6279\u53d1\u548c\u96f6\u552e\u4e1a"},{"priminducode":"14","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"14"},{"secnduname":"\u88c5\u5378\u642c\u8fd0\u548c\u8fd0\u8f93\u4ee3\u7406\u4e1a","secinducode":"1407"},{"secnduname":"\u6c34\u4e0a\u8fd0\u8f93\u4e1a","secinducode":"1405"},{"secnduname":"\u9053\u8def\u8fd0\u8f93\u4e1a","secinducode":"1403"}],"priminduname":"\u4ea4\u901a\u8fd0\u8f93\u3001\u4ed3\u50a8\u548c\u90ae\u653f\u4e1a"},{"priminducode":"13","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"13"},{"secnduname":"\u5efa\u7b51\u88c5\u9970\u548c\u5176\u4ed6\u5efa\u7b51\u4e1a","secinducode":"1303"},{"secnduname":"\u5efa\u7b51\u5b89\u88c5\u4e1a","secinducode":"1302"},{"secnduname":"\u571f\u6728\u5de5\u7a0b\u5efa\u7b51\u4e1a","secinducode":"1300"}],"priminduname":"\u5efa\u7b51\u4e1a"},{"priminducode":"12","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"12"},{"secnduname":"\u4fdd\u9669\u4e1a","secinducode":"1200"}],"priminduname":"\u91d1\u878d\u4e1a"},{"priminducode":"11","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"11"},{"secnduname":"\u71c3\u6c14\u751f\u4ea7\u548c\u4f9b\u5e94\u4e1a","secinducode":"1102"},{"secnduname":"\u6c34\u7684\u751f\u4ea7\u548c\u4f9b\u5e94\u4e1a","secinducode":"1101"},{"secnduname":"\u7535\u529b\u3001\u70ed\u529b\u751f\u4ea7\u548c\u4f9b\u5e94\u4e1a","secinducode":"1100"}],"priminduname":"\u7535\u529b\u3001\u70ed\u529b\u3001\u71c3\u6c14\u53ca\u6c34\u751f\u4ea7\u548c\u4f9b\u5e94\u4e1a"},{"priminducode":"10","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"10"},{"secnduname":"\u9910\u996e\u4e1a","secinducode":"1001"},{"secnduname":"\u4f4f\u5bbf\u4e1a","secinducode":"1000"}],"priminduname":"\u4f4f\u5bbf\u548c\u9910\u996e\u4e1a"},{"priminducode":"29","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"29"},{"secnduname":"\u6709\u8272\u91d1\u5c5e\u51b6\u70bc\u548c\u538b\u5ef6\u52a0\u5de5\u4e1a","secinducode":"2929"},{"secnduname":"\u94c1\u8def\u3001\u8239\u8236\u3001\u822a\u7a7a\u822a\u5929\u548c\u5176\u4ed6\u8fd0\u8f93\u8bbe\u5907\u5236\u9020\u4e1a","secinducode":"2928"},{"secnduname":"\u5bb6\u5177\u5236\u9020\u4e1a","secinducode":"2927"},{"secnduname":"\u5176\u4ed6\u5236\u9020\u4e1a","secinducode":"2926"},{"secnduname":"\u6728\u6750\u52a0\u5de5\u548c\u6728\u3001\u7af9\u3001\u85e4\u3001\u68d5\u3001\u8349\u5236\u54c1\u4e1a","secinducode":"2925"},{"secnduname":"\u4eea\u5668\u4eea\u8868\u5236\u9020\u4e1a","secinducode":"2922"},{"secnduname":"\u76ae\u9769\u3001\u6bdb\u76ae\u3001\u7fbd\u6bdb\u53ca\u5176\u5236\u54c1\u548c\u5236\u978b\u4e1a","secinducode":"2920"},{"secnduname":"\u519c\u526f\u98df\u54c1\u52a0\u5de5\u4e1a","secinducode":"2919"},{"secnduname":"\u533b\u836f\u5236\u9020\u4e1a","secinducode":"2918"},{"secnduname":"\u91d1\u5c5e\u5236\u54c1\u4e1a","secinducode":"2917"},{"secnduname":"\u6c7d\u8f66\u5236\u9020\u4e1a","secinducode":"2916"},{"secnduname":"\u98df\u54c1\u5236\u9020\u4e1a","secinducode":"2915"},{"secnduname":"\u9ed1\u8272\u91d1\u5c5e\u51b6\u70bc\u548c\u538b\u5ef6\u52a0\u5de5\u4e1a","secinducode":"2914"},{"secnduname":"\u975e\u91d1\u5c5e\u77ff\u7269\u5236\u54c1\u4e1a","secinducode":"2913"},{"secnduname":"\u5316\u5b66\u539f\u6599\u548c\u5316\u5b66\u5236\u54c1\u5236\u9020\u4e1a","secinducode":"2911"},{"secnduname":"\u5e9f\u5f03\u8d44\u6e90\u7efc\u5408\u5229\u7528\u4e1a","secinducode":"2910"},{"secnduname":"\u6587\u6559\u3001\u5de5\u7f8e\u3001\u4f53\u80b2\u548c\u5a31\u4e50\u7528\u54c1\u5236\u9020\u4e1a","secinducode":"2909"},{"secnduname":"\u901a\u7528\u8bbe\u5907\u5236\u9020\u4e1a","secinducode":"2908"},{"secnduname":"\u4e13\u7528\u8bbe\u5907\u5236\u9020\u4e1a","secinducode":"2907"},{"secnduname":"\u7eba\u7ec7\u4e1a","secinducode":"2906"},{"secnduname":"\u9020\u7eb8\u548c\u7eb8\u5236\u54c1\u4e1a","secinducode":"2905"},{"secnduname":"\u6a61\u80f6\u548c\u5851\u6599\u5236\u54c1\u4e1a","secinducode":"2904"},{"secnduname":"\u77f3\u6cb9\u52a0\u5de5\u3001\u70bc\u7126\u548c\u6838\u71c3\u6599\u52a0\u5de5\u4e1a","secinducode":"2903"},{"secnduname":"\u5370\u5237\u548c\u8bb0\u5f55\u5a92\u4ecb\u590d\u5236\u4e1a","secinducode":"2902"},{"secnduname":"\u7535\u6c14\u673a\u68b0\u548c\u5668\u6750\u5236\u9020\u4e1a","secinducode":"2901"},{"secnduname":"\u9152\u3001\u996e\u6599\u548c\u7cbe\u5236\u8336\u5236\u9020\u4e1a","secinducode":"2900"},{"secnduname":"\u8ba1\u7b97\u673a\u3001\u901a\u4fe1\u548c\u5176\u4ed6\u7535\u5b50\u8bbe\u5907\u5236\u9020\u4e1a","secinducode":"2930"}],"priminduname":"\u5236\u9020\u4e1a"},{"priminducode":"28","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"28"},{"secnduname":"\u623f\u5730\u4ea7\u4e1a","secinducode":"2800"}],"priminduname":"\u623f\u5730\u4ea7\u4e1a"},{"priminducode":"27","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"27"},{"secnduname":"\u5e7f\u64ad\u3001\u7535\u89c6\u3001\u7535\u5f71\u548c\u5f71\u89c6\u5f55\u97f3\u5236\u4f5c\u4e1a","secinducode":"2704"},{"secnduname":"\u5a31\u4e50\u4e1a","secinducode":"2703"},{"secnduname":"\u6587\u5316\u827a\u672f\u4e1a","secinducode":"2702"},{"secnduname":"\u65b0\u95fb\u548c\u51fa\u7248\u4e1a","secinducode":"2701"},{"secnduname":"\u4f53\u80b2","secinducode":"2700"}],"priminduname":"\u6587\u5316\u3001\u4f53\u80b2\u548c\u5a31\u4e50\u4e1a"},{"priminducode":"26","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"26"},{"secnduname":"\u4e13\u4e1a\u6280\u672f\u670d\u52a1\u4e1a","secinducode":"2602"},{"secnduname":"\u7814\u7a76\u548c\u8bd5\u9a8c\u53d1\u5c55","secinducode":"2601"},{"secnduname":"\u79d1\u6280\u63a8\u5e7f\u548c\u5e94\u7528\u670d\u52a1\u4e1a","secinducode":"2600"}],"priminduname":"\u79d1\u5b66\u7814\u7a76\u548c\u6280\u672f\u670d\u52a1\u4e1a"},{"priminducode":"25","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"25"},{"secnduname":"\u6559\u80b2","secinducode":"2500"}],"priminduname":"\u6559\u80b2"},{"priminducode":"24","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"24"},{"secnduname":"\u536b\u751f","secinducode":"2401"}],"priminduname":"\u536b\u751f\u548c\u793e\u4f1a\u5de5\u4f5c"},{"priminducode":"22","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"22"},{"secnduname":"\u519c\u4e1a","secinducode":"2204"},{"secnduname":"\u6e14\u4e1a","secinducode":"2203"},{"secnduname":"\u6797\u4e1a","secinducode":"2202"},{"secnduname":"\u755c\u7267\u4e1a","secinducode":"2201"},{"secnduname":"\u519c\u3001\u6797\u3001\u7267\u3001\u6e14\u670d\u52a1\u4e1a","secinducode":"2200"}],"priminduname":"\u519c\u3001\u6797\u3001\u7267\u3001\u6e14\u4e1a"},{"priminducode":"21","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"21"},{"secnduname":"\u7535\u4fe1\u3001\u5e7f\u64ad\u7535\u89c6\u548c\u536b\u661f\u4f20\u8f93\u670d\u52a1","secinducode":"2102"},{"secnduname":"\u4e92\u8054\u7f51\u548c\u76f8\u5173\u670d\u52a1","secinducode":"2100"}],"priminduname":"\u4fe1\u606f\u4f20\u8f93\u3001\u8f6f\u4ef6\u548c\u4fe1\u606f\u6280\u672f\u670d\u52a1\u4e1a"},{"priminducode":"20","seclist":[{"secnduname":"\u5168\u90e8","secinducode":"20"},{"secnduname":"\u673a\u52a8\u8f66\u3001\u7535\u5b50\u4ea7\u54c1\u548c\u65e5\u7528\u4ea7\u54c1\u4fee\u7406\u4e1a","secinducode":"2002"},{"secnduname":"\u5176\u4ed6\u670d\u52a1\u4e1a","secinducode":"2001"},{"secnduname":"\u5c45\u6c11\u670d\u52a1\u4e1a","secinducode":"2000"}],"priminduname":"\u5c45\u6c11\u670d\u52a1\u3001\u4fee\u7406\u548c\u5176\u4ed6\u670d\u52a1\u4e1a"}]}"""
_search_info = json.loads(_search_info)
_price = ["~100","100~200","200-500","500-1000","1000~"]
_year = ["1~","2~1","3~2","5~3","10~5","~10"]
_query = {
    "pageNum":"1",
    "pageSize":"20",
    "base":"bj",
    "estiblishTimeStart":"",
    "estiblishTimeEnd":"",
    "moneyStart":"",
    "moneyEnd":"",
    "city":"",
    "category":"",
}
_now = int(time.time()*1000)

def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj
def get_time(string):
    tmp_time = string.split("~")
    if tmp_time[0]:
    	st = _now-int(tmp_time[0])*31536000000
    else:
        st = ""
    if tmp_time[1]:
    	et = _now-int(tmp_time[1])*31536000000
    else:
        et = ""
    return st,et
    

class ListSpider(scrapy.Spider):
    name = "list"
    allowed_domains = []
    def __init__(self, *args, **kwargs):
        super(ListSpider, self).__init__(*args, **kwargs)
        self.surl = 'http://api.tianyancha.com/services/v3/search/%E5%AE%A0%E7%89%A9?{}'
        self.detail = 'http://api.tianyancha.com/services/v3/t/details/wapCompany/{}'
        self.start_urls = []

    def start_requests(self):
        for city in _search_info['city']:
            tmp_query = dict(_query)
            tmp_query['base'] = city
            tmp_query['pageNum'] = 1
            url = self.surl.format(urlencode(tmp_query))
            yield scrapy.Request(url,
                meta={"query":tmp_query},
                callback = self.parse
                )
    def detail_search(self,query):
        if query['moneyEnd'] or query['moneyStart']:
            self.logger.error("fuck we need more split"+json.dumps(query))
        elif query['estiblishTimeEnd'] or query['estiblishTimeStart']:
            for item in _price:
                tmp = item.split("~")
                tmp_query = dict(query)
                tmp_query['moneyStart'],tmp_query['moneyEnd'] = tmp
                url = self.surl.format(urlencode(tmp_query))
                yield scrapy.Request(url,
                    meta={"query":tmp_query},
                    callback = self.parse
                    )
        elif query['category']:
            for item in _year:
                tmp_query = dict(query)
                tmp_query['estiblishTimeStart'],tmp_query['estiblishTimeEnd'] = get_time(item)
                url = self.surl.format(urlencode(tmp_query))
                yield scrapy.Request(url,
                    meta={"query":tmp_query},
                    callback = self.parse
                    )
        elif query['city']:
            for item in _search_info['industry']:
                if item['primInduCode']:
                    tmp_query = dict(query)
                    tmp_query['category'] = item['primInduCode']
                    url = self.surl.format(urlencode(tmp_query))
                    yield scrapy.Request(url,
                        meta={"query":tmp_query},
                        callback = self.parse
                        )
        else:
            for item in _search_info['city'][query['base']]:
                if item == u"全部":
                    continue
                tmp_query = dict(query)
                tmp_query['city'] = item
                url = self.surl.format(urlencode(tmp_query))
                yield scrapy.Request(url,
                    meta={"query":tmp_query},
                    callback = self.parse
                    )
            
    def parse(self, response):
        self.logger.info(response.body)
        tmp_query = response.meta['query']
        bodys = json.loads(response.body)
        if bodys['state'] == "ok":
            if bodys['totalPage']*20 >= bodys['total']:
                yield self.detail_search(tmp_query)
            else:
                for item in bodys['data']:
                    if item['type'] == 1:
                        url = self.detail.format(item['id'])
                        yield scrapy.Request(url,
                            meta={"id":item['id']},
                            callback = self.parse_detail
                            )
                if bodys['totalPage'] > int(tmp_query['pageNum']):
                    tmp_query['pageNum'] = int(tmp_query['pageNum'])+1
                    url = self.surl.format(urlencode(tmp_query))
                    yield scrapy.Request(url,
                        meta={"query":tmp_query},
                        callback = self.parse
                        )
    def parse_detail(self, response):
        tmp = {}
        tmp['id'] = response.meta['id']
        tmp['content'] = response.body
        yield tmp
        
                
                
    
    
    
    
    