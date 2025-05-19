#include <vector>
#include <string>
#include <iostream>
using namespace std;

string check(vector<vector<char>> board)
{
    int n = board.size();

    //check row
    for(int i =0;i<n;++i)
    {
        int first = board[i][0];
        bool win = true;
        if(first == ' ')//skip this row
        {
            continue;
        }
        for(int j = 1;j<n;++j)
        {
            if(first != board[i][j])
            {
                win = false;
                break;
            }
        }
        //if that row is win
        if(win)
        {
            return string(1, first);
        }
    }

    //check col
   for(int i =0;i<n;++i)
    {
        int first = board[0][i];
        bool win = true;
        if(first == ' ')//skip this col
        {
            continue;
        }
        for(int j = 1;j<n;++j) //rows
        {
            if(first != board[j][i])
            {
                win = false;
                break;
            }
        }
        //if that row is win
        if(win)
        {
            return string(1, first);
        }
    }

    //check diagonals
    int first = board[0][0];
    if(first !=' ')
    {
        bool win = true;
        for(int i =1;i<n;++i)
        {
            if(board[i][i]!=first)
            {
                win = false;
                break;
            }
        }
        if(win)
        {
            return string(1, first);
        }
    }

    first = board[0][n-1];
    if(first !=' ')
    {
        bool win = true;
        for(int i =1;i<n;++i)
        {
            if(board[i][n-i-1]!=first)
            {
                win = false;
                break;
            }
        }
        if(win)
        {
            return string(1, first);
        }
    }

    //check for draw or pending
    for(int i=0;i<n;++i)
    {
        for(int j=0;j<n;++j)
        {
            if(board[i][j] ==' ')
            {
                return "pending";
            }
        }
    }

    return "Draw";
}

int main()
{
    vector<vector<char>> board = { {'X','O','X','O'},
        {'O','X','O','X'},
        {'O','X','X','O'},
        {'X','O','O','X'}};
    cout<<"Result = "<<check(board)<<endl;
}