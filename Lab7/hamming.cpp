#include<bits/stdc++.h>
using namespace std;

int main()
{
    int message[8]; //message bits are 7 6 5 4 3 2 1 out of which 4, 2, 1 are parity bits and other are data bits
    string str;
    cout<<"Enter the data to be sent(4 bits)"<<endl;
    cin>>str;
    message[7]=str[0]-'0';
    message[6]=str[1]-'0';
    message[5]=str[2]-'0';
    message[3]=str[3]-'0';

    //calculating parity bits
    message[4]=message[7]^message[6]^message[5];
    message[2]=message[7]^message[6]^message[3];
    message[1]=message[7]^message[5]^message[3];

    cout<<"Message sent:"<<endl;
    for(int i=7;i>=1;i--)
    {
        cout<<message[i];
    }
    cout<<endl;

    //take received message as input and check for errors
    cout<<"Enter the message received"<<endl;
    cin>>str;
    int msgrcv[8];

    //converting string to array of message bits 7 6 5 4 3 2 1
    for(int i=1;i<=7;i++)
    {
        msgrcv[i]=str[7-i]-'0';
    }

    //compute a3 a2 a1 to check for errors
    int a3=msgrcv[4]^msgrcv[7]^msgrcv[6]^msgrcv[5];
    int a2=msgrcv[2]^msgrcv[7]^msgrcv[6]^msgrcv[3];
    int a1=msgrcv[1]^msgrcv[7]^msgrcv[5]^msgrcv[3];
    int error= a3*4+a2*2+a1;
    if(error==0)
    {
        cout<<"No error detected"<<endl;
    }
    else
    {
        cout<<"Error found at bit "<<error<<endl;
        cout<<"Corrected message:"<<endl;
        //flip the bit corresponding to the error bit
        for(int i=7;i>=1;i--)
        {
            if(i==error)
                cout<<1-msgrcv[i];
            else
                cout<<msgrcv[i];
        }
        cout<<endl;
    }
    return 0;
}
