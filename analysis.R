library(readxl)
library(zoo)
library(openxlsx)
library(forecast)
library(lmtest)
library(tseries)
library(ggplot2)
library(scales)
library(psych)


# Functions ----------------------------
mutate_data <- function(df) {
    dn <- ts(df, start = c(1996), frequency = 1)
    dnt <- window(dn, end = 2019)
    
    return(data.frame(dn, dnt))
}

gcast <- function(dn, fcast) {
    
    en <- max(time(fcast$mean)) # extract the max date used in the forecast
    
    #Extract Source and Training Data
    ds <- as.data.frame(window(dn, end = en, extend = TRUE))
    names(ds) <- 'observed'
    ds$date <- as.Date(time(window(dn, end = en, extend = TRUE)))
    
    # Extract the Fitted Values (need to figure out how to grab confidence intervals)
    dfit <- as.data.frame(fcast$fitted)
    dfit$date <- as.Date(time(fcast$fitted))
    names(dfit)[1] <- 'fitted'
    
    ds <- merge(ds, dfit, all.x = TRUE) # Merge fitted values with source and training data
    
    # Exract the Forecast values and confidence intervals
    dfcastn <- as.data.frame(fcast)
    dfcastn$date <- as.Date(as.yearmon(as.numeric(row.names(dfcastn))))
    names(dfcastn) <- c('forecast','lo80','hi80','lo95','hi95','date')
    
    pd <- merge(ds, dfcastn, all.x = TRUE) # final data.frame for use in ggplot
    return(pd)
    
}

get_plot <- function(df, name) {
    p1a <- ggplot(data = df, aes(x = date, y = observed)) 
    p1a <- p1a + geom_point(col = 'purple') + ggtitle(paste('Prediction for', name), subtitle = 'Purple - data points, black - forecasted points, shadow - 95% conf. interval')
    p1a <- p1a + xlab('Year')
    p1a <- p1a + ylab('Value')
    p1a <- p1a + geom_point(aes(y = forecast)) + geom_ribbon(aes(ymin = lo95, ymax = hi95), alpha = 0.25)
    p1a <- p1a + theme_bw()
    
    return(p1a)
}


# Data manipulation --------------------

data_transp_for_analysis <- read_excel("/Users/stanislavermohin/Desktop/NSU/Thesis/xlsx_output/data_transp_for_analysis.xlsx", 
                                       col_types = c("numeric", "numeric", "numeric", 
                                                     "numeric", "numeric", "numeric", 
                                                     "numeric"))
data <- data.frame(na.spline.default(data_transp_for_analysis))
# write.xlsx(data, file = '~/Desktop/NSU/Thesis/data_splined.xlsx')
real_names <- data.frame(name = names(data))
row.names(real_names) <- c('deflator', 'gdp', 'r&d', 'cuip', 'pa', 'fbs', 'ict')
names(data) <- rownames(real_names)
# View(data)

test_for_diffs <- data.frame(name = names(data), adf = NA, kpss = NA, pp = NA)
test_for_diffs$adf <- apply(data, 2, ndiffs, test = 'adf')
test_for_diffs$kpss <- apply(data, 2, ndiffs, test = 'kpss')
test_for_diffs$pp <- apply(data, 2, ndiffs, test = 'adf')
row.names(test_for_diffs) <- test_for_diffs$name
test_for_diffs <- subset(test_for_diffs, select = -c(name))
test_for_diffs$max <- apply(test_for_diffs, 1, max)

data_diff1 <- data[test_for_diffs$max == 1]
row.names(data_diff1) <- 1996:2019
data_diff2 <- data[test_for_diffs$max == 2]
row.names(data_diff2) <- 1996:2019
defed_data_1 <- data.frame(diff(as.matrix(data_diff1),
                                differences = 1))
defed_data_2 <- data.frame(diff(as.matrix(data_diff2),
                                differences = 2))
defed_data <- data.frame(defed_data_1[2:NROW(defed_data_1), ],
                         defed_data_2)
# View(defed_data)
# View(test_for_diffs)
apply(defed_data, 2, acf)

defed_toI1_data <- data.frame(data_diff1[2:NROW(data_diff1), ],
                              diff(as.matrix(data_diff2), differences = 1))
# View(defed_toI1_data)
acf_data <- apply(defed_toI1_data, 2, acf, plot = FALSE, lag.max = 23) # all stationary (ro(k) (k -> Inf) -> 0) => all data ~ I(1)
acf_data$`r&d` <- acf_data$`r.d`



# Check for I(1) with ACF --------------

for (col in names(acf_data)) {
    all <- data.frame(x = acf_data[[col]]$lag, y = acf_data[[col]]$acf)
    plot <- ggplot(all, aes(x = x, y = y)) + geom_line(aes(y = y), color = 'purple') +
        ggtitle(paste('ACF function for the first difference of'), subtitle = real_names$name[rownames(real_names) == col]) +
        ylab('ACF') +
        xlab('Lag') +
        theme_bw() +
        geom_hline(yintercept = 0, color = 'light blue')
    print(plot)
}

# Using data itself (no differencing) for co-integration tests

# Co-integration test ------------------

gdp <- data$gdp
needed_data <- subset(data, select = -c(gdp, deflator))
# View(needed_data)
coint_res <- data.frame(t = 1996:2019)

coint_lambda <- data.frame(t = 1996:2019)

for (column in names(needed_data)) {
    fit <- lm(scale(gdp, scale = FALSE)~scale(needed_data[[column]], scale = FALSE))
    print(column)
    # print(bptest(fit))
    # print(summary(fit))
    coint_res[[column]] <- fit$residuals
    coint_lambda[[column]] <- fit$coefficients[[2]]
    a <- acf(fit$residuals,
             lag.max = NROW(fit$residuals),
             plot = FALSE)
    all <- data.frame(x = a$lag, y = a$acf)
    plot <- ggplot(all, aes(x = x, y = y)) + geom_line(aes(y = y), color = 'purple') +
        ggtitle(paste('ACF function for'), subtitle = real_names$name[rownames(real_names) == column]) +
        ylab('ACF') +
        xlab('Lag') +
        theme_bw() +
        geom_hline(yintercept = 0, color = 'light blue')
    # print(plot)
    
}


# ARIMA --------------------------------
forecasts <- data.frame(t = c(2020:2022,
                              'l802020', 'l952020',
                              'l802021', 'l952021',
                              'l802022', 'l952022'))

arima_fit_gdp <- auto.arima(gdp, max.p = 3, max.q = 3, d = 1, ic = 'aic')
summary(arima_fit_gdp)
coeftest(arima_fit_gdp)
prediction_gdp <- forecast(arima_fit_gdp, 3)
forecasts[['gdp']] <- prediction_gdp[[4]][1:3]
needed_data <- subset(data, select = -c(deflator, gdp))

for (col in names(needed_data)) {
    print(col)
    arima_fit <- auto.arima(needed_data[[col]], max.p = 3, max.q = 3, d = 1, ic = 'aic')
    print(coeftest(arima_fit))
    prediction <- forecast(arima_fit, 3)
    forecasts[[col]] <- c(prediction[[4]][1:3], prediction[[5]][1:3], prediction[[6]][1:3])
}
# write.xlsx(forecasts, '~/Desktop/NSU/Thesis/forecasts.xlsx')


# Plot forecast --------------------
all <- subset(data, select = -c(deflator))

for (column in names(all)) {
    data_to_go <- mutate_data(all[[column]])
    arima_fit <- auto.arima(data_to_go$dnt, max.p = 3, max.q = 3, d = 1, ic = 'aic')
    yfor <- forecast(arima_fit, 3)
    pd <- gcast(data_to_go$dn, yfor)
    plot <- get_plot(pd, column)
    print(plot)
    
}




# ECM ----------------------------------
corr_matrix <- cor(subset(all))
# View(corr_matrix)
# write.xlsx(corr_matrix, file = '~/Desktop/NSU/Thesis/corr_matrix.xlsx')
all$rd <- all$`r&d`
data_go <- read_excel("~/Desktop/NSU/Thesis/to_analyze_data.xlsx", 
                      col_types = c("numeric", "numeric", "numeric", 
                                    "numeric"))
data_go <- data.frame(data_go)

actual_fit <- lm(data = data_go, gdpd~res1+gdpd1+cuipd1)
summary(actual_fit) # oh, yeeeeees, it's worked

# ECM prediction -----------------------
next_gdpd <- predict.lm(actual_fit, newdata = data.frame(res1 = 1.31374812, gdpd1 = -0.015568068, cuipd1 = -6.166148502))
next_gdp_1 <- harmonic.mean(c(next_gdpd + data$gdp[NROW(data$gdp)], forecasts$gdp[1]))
next_gdp_2 <- geometric.mean(c(next_gdpd + data$gdp[NROW(data$gdp)], forecasts$gdp[1]))
next_gdp_3 <- mean(c(next_gdpd + data$gdp[NROW(data$gdp)], forecasts$gdp[1]))
# View(c(next_gdp_1, next_gdp_2, next_gdp_3))






