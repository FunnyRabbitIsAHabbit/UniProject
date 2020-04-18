library(forecast)
library(readxl)
library(openxlsx)

data_transp_for_analysis <- read_excel("~/Desktop/NSU/Thesis/data_transp_for_analysis.xlsx", 
                                       col_types = c("numeric", "numeric", "numeric", 
                                                     "numeric", "numeric", "numeric", 
                                                     "numeric"))
data_arima <- data.frame(data_transp_for_analysis)
data_arima$Fixed.broadband.subscriptions[24] <- forecast(auto.arima(data_arima$Fixed.broadband.subscriptions), 1)[[4]][1]
data_arima$Charges.for.the.use.of.intellectual.property..payments..BoP..constant.2019.bln..usd.[24] <- forecast(auto.arima(data_arima$Charges.for.the.use.of.intellectual.property..payments..BoP..constant.2019.bln..usd.), 1)[[4]][1]
data_arima$Patent.applications..total[24] <- forecast(auto.arima(data_arima$Patent.applications..total), 1)[[4]][1]
data_arima$Research.and.development.expenditure..total..constant.2019.bln..usd.[23] <- forecast(auto.arima(data_arima$Research.and.development.expenditure..total..constant.2019.bln..usd.), 1)[[4]][1]
data_arima$Research.and.development.expenditure..total..constant.2019.bln..usd.[24] <- forecast(auto.arima(data_arima$Research.and.development.expenditure..total..constant.2019.bln..usd.), 2)[[4]][2]
data_arima$ICT.service.exports..BoP..constant.2019.bln..US..[23] <- forecast(auto.arima(data_arima$ICT.service.exports..BoP..constant.2019.bln..US..), 1)[[4]][1]
data_arima$ICT.service.exports..BoP..constant.2019.bln..US..[24] <- forecast(auto.arima(data_arima$ICT.service.exports..BoP..constant.2019.bln..US..), 2)[[4]][2]
data_arima$Fixed.broadband.subscriptions <- na.spline.default(data_arima$Fixed.broadband.subscriptions)
View(data_arima)

write.xlsx(data, file = '~/Desktop/NSU/Thesis/data_forecasted.xlsx')
