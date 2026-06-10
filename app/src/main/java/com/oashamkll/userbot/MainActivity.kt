package com.oashamkll.userbot

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.snackbar.Snackbar
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout

class MainActivity : AppCompatActivity() {

    private lateinit var sharedPreferences: SharedPreferences

    // UI elements
    private lateinit var loginFormContainer: LinearLayout
    private lateinit var verificationContainer: LinearLayout
    private lateinit var dashboardContainer: LinearLayout

    private lateinit var apiIdInput: TextInputEditText
    private lateinit var apiHashInput: TextInputEditText
    private lateinit var phoneInput: TextInputEditText
    private lateinit var codeInput: TextInputEditText
    private lateinit var passwordInput: TextInputEditText
    private lateinit var passwordInputLayout: TextInputLayout

    private lateinit var requestCodeBtn: Button
    private lateinit var loginBtn: Button
    private lateinit var pingBtn: Button
    private lateinit var parseBtn: Button
    private lateinit var logoutBtn: Button

    private lateinit var statusText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        sharedPreferences = getSharedPreferences("UserBotStorage", Context.MODE_PRIVATE)

        // Initialize UI
        loginFormContainer = findViewById(R.id.loginFormContainer)
        verificationContainer = findViewById(R.id.verificationContainer)
        dashboardContainer = findViewById(R.id.dashboardContainer)

        apiIdInput = findViewById(R.id.apiIdInput)
        apiHashInput = findViewById(R.id.apiHashInput)
        phoneInput = findViewById(R.id.phoneInput)
        codeInput = findViewById(R.id.codeInput)
        passwordInput = findViewById(R.id.passwordInput)
        passwordInputLayout = findViewById(R.id.passwordInputLayout)

        requestCodeBtn = findViewById(R.id.requestCodeBtn)
        loginBtn = findViewById(R.id.loginBtn)
        pingBtn = findViewById(R.id.pingBtn)
        parseBtn = findViewById(R.id.parseBtn)
        logoutBtn = findViewById(R.id.logoutBtn)

        statusText = findViewById(R.id.statusText)

        // Load saved credentials
        loadSavedCredentials()

        // Set up Listeners
        requestCodeBtn.setOnClickListener {
            handleRequestCode()
        }

        loginBtn.setOnClickListener {
            handleLogin()
        }

        pingBtn.setOnClickListener {
            showSnackbar("👋 Пинг отправлен в Избранное!", true)
        }

        parseBtn.setOnClickListener {
            showSnackbar("👥 Ваши чаты: Новости, Семья, Работа...", true)
        }

        logoutBtn.setOnClickListener {
            handleLogout()
        }
    }

    private fun loadSavedCredentials() {
        val savedApiId = sharedPreferences.getString("api_id", "")
        val savedApiHash = sharedPreferences.getString("api_hash", "")
        val savedPhone = sharedPreferences.getString("phone", "")

        apiIdInput.setText(savedApiId)
        apiHashInput.setText(savedApiHash)
        phoneInput.setText(savedPhone)
    }

    private fun handleRequestCode() {
        val apiId = apiIdInput.text.toString().trim()
        val apiHash = apiHashInput.text.toString().trim()
        val phone = phoneInput.text.toString().trim()

        if (apiId.isEmpty() || apiHash.isEmpty() || phone.isEmpty()) {
            statusText.text = "Ошибка: заполните все поля!"
            statusText.setTextColor(resources.getColor(android.R.color.holo_red_light, theme))
            return
        }

        // Save credentials
        sharedPreferences.edit().apply {
            putString("api_id", apiId)
            putString("api_hash", apiHash)
            putString("phone", phone)
            apply()
        }

        statusText.text = "Подключение к API Telegram..."
        statusText.setTextColor(resources.getColor(android.R.color.holo_orange_light, theme))

        // Simulate network delay
        requestCodeBtn.postDelayed({
            statusText.text = "Код отправлен в Telegram!"
            statusText.setTextColor(resources.getColor(android.R.color.holo_orange_light, theme))

            loginFormContainer.visibility = View.GONE
            verificationContainer.visibility = View.VISIBLE
        }, 1500)
    }

    private fun handleLogin() {
        val code = codeInput.text.toString().trim()

        if (code.isEmpty()) {
            statusText.text = "Ошибка: введите код подтверждения!"
            statusText.setTextColor(resources.getColor(android.R.color.holo_red_light, theme))
            return
        }

        // Simulate 2FA cloud password challenge
        if (passwordInputLayout.visibility == View.GONE && code == "12345") {
            statusText.text = "Требуется облачный пароль (2FA)!"
            statusText.setTextColor(resources.getColor(android.R.color.holo_orange_light, theme))
            passwordInputLayout.visibility = View.VISIBLE
            return
        }

        statusText.text = "Вход в аккаунт..."
        statusText.setTextColor(resources.getColor(android.R.color.holo_green_light, theme))

        loginBtn.postDelayed({
            statusText.text = "Успешная авторизация!"
            statusText.setTextColor(resources.getColor(android.R.color.holo_green_light, theme))

            verificationContainer.visibility = View.GONE
            dashboardContainer.visibility = View.VISIBLE
        }, 1200)
    }

    private fun handleLogout() {
        // Clear code & password fields
        codeInput.text?.clear()
        passwordInput.text?.clear()
        passwordInputLayout.visibility = View.GONE

        dashboardContainer.visibility = View.GONE
        verificationContainer.visibility = View.GONE
        loginFormContainer.visibility = View.VISIBLE

        statusText.text = "Введите данные для входа"
        statusText.setTextColor(resources.getColor(android.R.color.darker_gray, theme))
    }

    private fun showSnackbar(message: String, success: Boolean) {
        val view = findViewById<View>(android.R.id.content)
        val snackbar = Snackbar.make(view, message, Snackbar.LENGTH_LONG)
        val snackbarView = snackbar.view
        if (success) {
            snackbarView.setBackgroundColor(resources.getColor(android.R.color.holo_green_dark, theme))
        } else {
            snackbarView.setBackgroundColor(resources.getColor(android.R.color.holo_red_dark, theme))
        }
        snackbar.show()
    }
}
