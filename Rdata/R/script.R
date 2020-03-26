#!/usr/bin/env Rscript

library(magrittr);
library(tidyverse)
library(ggplot2)

df = read.csv("./Rdata/R/raw_data.csv", header = TRUE, sep = ";")

df1 <- df %>%
  select(city_name, city_cod, state, state_cod) %>%
  unique() %>%
  filter( state_cod != "None") %>%
  arrange(city_name)

write.csv(df1,"code_table.csv", row.names = FALSE)


df2 <- df %>%
  select(date, new_cases) %>%
  arrange(date) %>%
  group_by(date) %>%
  summarise(new_cases = sum(new_cases)) %>%
  mutate(total_cases=cumsum(new_cases))

df3 <- df2 %>% filter( date != "Não informado") %>% ggplot( aes(x = factor(date), y = total_cases)) +
  geom_line(aes(group=1)) + theme_bw() + theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(x="Data", y="N casos", title="Crescimento Covid19 no Brasil.") +
  theme(plot.title = element_text(hjust = 0.5)) +
  ggsave('./data/cases_brasil.png', width = 20, height = 9, dpi = 100)

df4 <- df2 %>% filter( date != "Não informado") %>% ggplot(aes(x = date, y = new_cases)) +
  geom_bar(stat="identity", fill="black") +
  labs(y = "Casos Novos", x = "Data", title = "Novos Casos de Covid19 Brasil") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  ggsave('./data/new_cases_brasil.png', width = 20, height = 9, dpi = 100)

df5 <- df %>%
  group_by(state) %>%
  summarise(total_casos = sum(new_cases)) %>%
  arrange(desc(total_casos))

#write.csv(df5, "../../data/cases_states.csv", row.names = FALSE)

Sys.setenv(TZ = "GMT+3")
today <- format(Sys.Date(), format="%Y-%m-%d")

df6 <- df %>%
  filter(date == today) %>%
  select(new_cases, state) %>%
  group_by(state) %>%
  summarise(new_cases = sum(new_cases))


res <- merge(df6, df5, all = TRUE)
res[is.na(res)] <- 0
write.csv(res, "./data/cases_states.csv", row.names = FALSE)

splitdf <- df %>% select(state, city_name, date, new_cases, count)  %>% split(df$state)
lapply(names(splitdf), function(x){

  tmp1 <- splitdf[[x]] %>% select(city_name, new_cases) %>%
    group_by(city_name) %>%
    summarise(total_casos = sum(new_cases)) %>%
    arrange(desc(total_casos))

  tmp2 <- df %>%
    filter(date == today) %>%
    select(new_cases, city_name) %>%
    group_by(city_name) %>%
    summarise(new_cases = sum(new_cases))

  res <- merge(tmp1, tmp2, all = TRUE)
  res[is.na(res)] <- 0

  write.csv(res, file = paste("./data/",x ,"/cases_", x, ".csv", sep = ""), row.names = FALSE)
  write.csv((splitdf[[x]] %>% arrange(city_name, date)), file = paste("./data/",x ,"/cities_cases_", x, ".csv", sep = ""), row.names = FALSE)
  Sys.setenv(TZ = "GMT+3")
  today <- format(Sys.Date(), format="%Y-%m-%d")
  Sys.time()
  })
