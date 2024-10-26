using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Numerics;

public class sGold : MonoBehaviour
{
    public ResourceHandler resourceHandler; // Reference to ResourceHandler script
    public Text goldText;

    private BigInteger septillion = BigInteger.Pow(10, 24); // Value for septillion with 24 zeros

    public void Update()
    {
        // Get the gold value from the ResourceHandler script
        BigInteger gold = resourceHandler.Gold;

        // Check gold
        Debug.Log("Gold: " + gold.ToString());

        // Format the gold value with appropriate prefix
        string formattedGold = FormatGoldNumber(gold);

        // Update the gold text UI element with the new gold value
        goldText.text = formattedGold;
    }

    // Function to format a BigInteger number with appropriate prefix
    private string FormatGoldNumber(BigInteger number)
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

