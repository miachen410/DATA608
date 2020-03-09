library(shiny)
library(tidyverse)
library(rsconnect)

# Read in data
cdc <- read_csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")


# Define UI for application that shows a barplot
ui <- fluidPage(
  
  titlePanel("Mortality Rates by State in 2010"),

  sidebarLayout(
    sidebarPanel(
      helpText("Select a cause to see States ranked by crude mortality"),
      uiOutput("causeOutput")
    ),
    
    mainPanel(
      plotOutput("barplot")
    )
  )
)

# Define server logic required to show a barplot
server <- function(input, output) {
  output$causeOutput <- renderUI({
    selectInput("causeInput", "Cause",
                unique(cdc$ICD.Chapter),
                selected = "Neoplasms")
  })
  output$barplot <- renderPlot({
    cdc %>% 
      filter(Year == "2010", ICD.Chapter == input$causeInput) %>% 
      group_by(State) %>%
      ggplot(aes(x = reorder(State, Crude.Rate), y = Crude.Rate)) +
        geom_bar(stat = "identity") +
        coord_flip() +
        ylab("Crude Mortality Rate") +
        xlab("State")
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
