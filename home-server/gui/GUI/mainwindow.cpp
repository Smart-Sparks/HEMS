#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QSqlDatabase>
#include <QSqlError>
#include <QSqlQuery>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // Connect to Database
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_clicked()
{
    // toggle power for the selected device
}

void MainWindow::on_listWidget_itemDoubleClicked(QListWidgetItem *item)
{
    // change main window to reflect information about this item
}

bool MainWindow::connectDatabase()
{
    // connects to the HEMS database
    QSqlDatabase db = QSqlDatabase::addDatabase("MDB");
    db.setDatabaseName("HEMS");
    db.setUserName("root");
    db.setPassword("");
    db.setHostName("localhost");

    // bool ok = db.open();

}
