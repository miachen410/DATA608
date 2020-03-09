library(shiny)
library(tidyverse)

# Read in data
cdc <- read_csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")


# Define UI for application that draws the line plot
ui <- fluidPage(
  titlePanel("State Mortality Rates vs National Average"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Select cause and state to view the state crude mortality rate 
               vs national average over time."),
      uiOutput("causeOutput"),
      uiOutput("stateOutput")
    ),
    mainPanel(
      plotOutput("stateplot")
    )
  )
)

# Define server logic required to show a line plot
server <- function(input, output) {
  output$causeOutput <- renderUI({
    selectInput("causeInput", "Cause",
                unique(cdc$ICD.Chapter),
                selected = "Neoplasms")
  })
  
  output$stateOutput <- renderUI({
    selectInput("stateInput", "State",
                unique(cdc$State),
                selected = "NY")
  })

  cdc_cause <- reactive({
    if (is.null(input$causeInput)) {
      return(NULL)
    }
    cdc %>%
      filter(ICD.Chapter == input$causeInput)
  })
  
  cdc_avg <- reactive({
    if (is.null(input$causeInput)) {
      return(NULL)
    }
    cdc_cause() %>%
      group_by(Year) %>%
      summarize(totalDeath = sum(Deaths), totalPopulation = sum(Population)) %>%
      mutate(NationalAvg = totalDeath*100000/totalPopulation) 
      #crude death rate is total death over total population, multiplied by 100,000
  })
  
  state <- reactive({
    if (is.null(input$stateInput)) {
      return(NULL)
    }
    cdc_cause() %>% filter(State == input$stateInput)
  })
  
  output$stateplot <- renderPlot({
    if (is.null(cdc_cause())) {
      return()
    }
    ggplot() +
      geom_line(data = state(), aes(x = Year, y = Crude.Rate, color = "red")) +
      geom_line(data = cdc_avg(), aes(x = Year, y = NationalAvg, color = "blue")) +
      labs(title = input$causeInput, x = "", y = "") +
      scale_color_discrete(labels = c("State", "Nation"))
  })
}

# Run the application 
shinyApp(ui = ui, server = server)
