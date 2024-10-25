using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Numerics;

public class sLog : MonoBehaviour
{
    public ResourceHandler resourceHandler; // Reference to ResourceHandler script
    public Text logText;

    private BigInteger septillion = BigInteger.Pow(10, 24); // Value for septillion with 24 zeros

    public void Update()
    {
        // Get the logs value from the ResourceHandler script
        BigInteger log = resourceHandler.Wood;

        // Check logs
        Debug.Log("Logs: " + log.ToString());

        // Format the logs value with appropriate prefix
        string formattedLog = FormatLogNumber(log);

        // Update the logs text UI element with the new logs value
        logText.text = formattedLog;
    }

    // Function to format a BigInteger number with appropriate prefix
    private string FormatLogNumber(BigInteger number)
    {
        if (number >= septillion)
        {
            return (number / septillion).ToString() + " Sp";
        }
        else if (number >= BigInteger.Pow(10, 21))
        {
            return (number / BigInteger.Pow(10, 21)).ToString() + " Sx";
        }
        else if (number >= BigInteger.Pow(10, 18))
        {
            return (number / BigInteger.Pow(10, 18)).ToString() + " Qi";
        }
        else if (number >= BigInteger.Pow(10, 15))
        {
            return (number / BigInteger.Pow(10, 15)).ToString() + " Qa";
        }
        else if (number >= BigInteger.Pow(10, 12))
        {
            return (number / BigInteger.Pow(10, 12)).ToString() + " T";
        }
        else if (number >= BigInteger.Pow(10, 9))
        {
            return (number / BigInteger.Pow(10, 9)).ToString() + " B";
        }
        else if (number >= BigInteger.Pow(10, 6))
        {
            return (number / BigInteger.Pow(10, 6)).ToString() + " M";
        }
        else if (number >= BigInteger.Pow(10, 3))
        {
            return (number / BigInteger.Pow(10, 3)).ToString() + " K";
        }
        else
        {
            return number.ToString();
        }
    }
}
