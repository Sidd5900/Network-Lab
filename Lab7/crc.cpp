#include<bits/stdc++.h>
using namespace std;

//calculate xor of two strings excluding the first character
string xorfunc(string a, string b)
{
    string ans = "";
    int n = b.length();
    for(int i = 1; i < n; i++)
    {
        int x=(a[i]-'0')^(b[i]-'0');
        ans+=(x+'0');
    }
    return ans;
}

//modulo 2 division is done which finally returns the remainder in the form of string
string divide(string dividend, string divisor)
{
    int next = divisor.length();    //next bit to be pull down while dividing
    string tmp = dividend.substr(0, next);  //initial dividend
    int dividendLen = dividend.length();

    //traverse the dividend bit by bit
    while (next < dividendLen)
    {
        if (tmp[0] == '1')
            //change dividend to remainder + the next bit of the original dividend
            tmp = xorfunc(divisor, tmp) + dividend[next];
        else
            //take xor with all zeros
            tmp = xorfunc(std::string(next, '0'), tmp) + dividend[next];
        next++;
    }

    // For the last n bits repeating the same process as index goes out of bound
    if (tmp[0] == '1')
        tmp = xorfunc(divisor, tmp);
    else
        tmp = xorfunc(std::string(next, '0'), tmp);

    return tmp; //the last dividend is the required remainder
}

//encode the input data using crc and return the encoded message
string encodeData(string &data, string &divisor)
{
    int n=divisor.size();
    string append="";

    //append n-1 zeroes
    for(int i=0;i<n-1;i++)
        append+='0';
    string appendData= data+append;
    string rem= divide(appendData,divisor);
    //append remainder at the end of original data and return
    return data+rem;

}

int main()
{
    string data;
    cout<<"Enter the data to be encoded:"<<endl;
    cin>>data;
    string divisor="1001";  //fixing a 4 bit divisor
    int divisorLen=divisor.size();
    string enc=encodeData(data,divisor);
    cout<<"Encode data:"<<endl;
    cout<<enc<<endl;

    //check for errors in the message received
    string msgrcv;
    cout<<"Enter the message received"<<endl;
    cin>>msgrcv;
    string rem=divide(msgrcv,divisor);      //find remainder for the received message and given divisor
    string requiredrem="";
    for(int i=0;i<divisorLen-1;i++)
        requiredrem+="0";
    if(rem==requiredrem)
        cout<<"No error detected"<<endl;
    else
        cout<<"Error detected"<<endl;

    return 0;
}
